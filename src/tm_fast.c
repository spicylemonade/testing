/*
 * Fast Turing Machine simulator in C.
 * Compiled as a shared library for use from Python via ctypes.
 *
 * Compile: gcc -O3 -shared -fPIC -o tm_fast.so tm_fast.c
 */

#include <stdlib.h>
#include <string.h>

/* Result structure */
typedef struct {
    long long steps;
    long long ones;
    int halted;
} TMResult;

/*
 * Simulate a Turing machine.
 *
 * transition_table: flat array of (write, direction, next_state) triples.
 *   Index: (state * 2 + symbol) * 3 + {0=write, 1=direction(+1/-1), 2=next_state}
 *   Use next_state = -1 for halt.
 * num_states: number of states (excluding halt)
 * max_steps: maximum simulation steps
 * result: output structure
 */
void tm_simulate(const int *transition_table, int num_states, long long max_steps, TMResult *result) {
    /* Tape: dynamically growing array */
    int tape_size = 2000000;  /* 2M cells initial */
    unsigned char *tape = (unsigned char *)calloc(tape_size, 1);
    if (!tape) {
        result->steps = 0;
        result->ones = 0;
        result->halted = 0;
        return;
    }

    int head = tape_size / 2;
    int state = 0;  /* State A = 0 */
    long long steps = 0;
    int halted = 0;

    int lo = 1000;
    int hi = tape_size - 1000;

    /*
     * Tight inner loop: batch process steps without bounds checking.
     * Only check tape bounds every BATCH_SIZE steps.
     */
    #define BATCH_SIZE 10000

    while (steps < max_steps) {
        long long batch_end = steps + BATCH_SIZE;
        if (batch_end > max_steps) batch_end = max_steps;

        /* Check if we have room for BATCH_SIZE moves in either direction */
        if (head < lo || head >= hi) {
            /* Need to expand */
            if (head < lo) {
                int ext = tape_size;
                int new_size = tape_size + ext;
                unsigned char *new_tape = (unsigned char *)calloc(new_size, 1);
                if (!new_tape) break;
                memcpy(new_tape + ext, tape, tape_size);
                free(tape);
                tape = new_tape;
                head += ext;
                tape_size = new_size;
            } else {
                int ext = tape_size;
                int new_size = tape_size + ext;
                unsigned char *new_tape = (unsigned char *)realloc(tape, new_size);
                if (!new_tape) break;
                memset(new_tape + tape_size, 0, ext);
                tape = new_tape;
                tape_size = new_size;
            }
            lo = 1000;
            hi = tape_size - 1000;
        }

        /* Fast inner loop without bounds checking */
        while (steps < batch_end) {
            int symbol = tape[head];
            const int *entry = transition_table + (state * 2 + symbol) * 3;
            int write = entry[0];
            int dir = entry[1];
            int next = entry[2];

            if (next < 0) {
                tape[head] = (unsigned char)write;
                steps++;
                halted = 1;
                goto done;
            }

            tape[head] = (unsigned char)write;
            head += dir;
            state = next;
            steps++;
        }
    }

done:
    /* Count ones using SIMD-friendly loop */
    {
        long long ones = 0;
        int i;
        for (i = 0; i + 8 <= tape_size; i += 8) {
            ones += tape[i] + tape[i+1] + tape[i+2] + tape[i+3]
                  + tape[i+4] + tape[i+5] + tape[i+6] + tape[i+7];
        }
        for (; i < tape_size; i++) {
            ones += tape[i];
        }

        result->steps = steps;
        result->ones = ones;
        result->halted = halted;
    }

    free(tape);
}
