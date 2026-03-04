# Benchmark Corpus

Total files: 20

| File | Category | Original Size | Compressed (L6) | Ratio |
|------|----------|---------------|-----------------|-------|
| rle_single.bin | adversarial | 262,144 | 272 | 0.1% |
| pattern_repeat.bin | adversarial | 262,144 | 540 | 0.2% |
| mixed_entropy.bin | adversarial | 262,144 | 159,042 | 60.7% |
| binary_elf.bin | binary | 230,404 | 205,365 | 89.1% |
| binary_wasm.bin | binary | 50,008 | 50,028 | 100.0% |
| random_bytes.bin | binary | 262,144 | 262,224 | 100.0% |
| structured_binary.bin | binary | 120,008 | 3,310 | 2.8% |
| text_1k.txt | size_variant | 1,024 | 334 | 32.6% |
| text_4k.txt | size_variant | 4,096 | 1,022 | 25.0% |
| text_16k.txt | size_variant | 16,384 | 3,409 | 20.8% |
| text_64k.txt | size_variant | 65,536 | 11,841 | 18.1% |
| text_1024k.txt | size_variant | 1,048,576 | 176,943 | 16.9% |
| english_prose.txt | text | 262,144 | 51,636 | 19.7% |
| source_code.c | text | 262,144 | 23,782 | 9.1% |
| structured.json | text | 262,144 | 35,929 | 13.7% |
| markup.xml | text | 262,144 | 27,531 | 10.5% |
| tabular.csv | text | 257,803 | 92,632 | 35.9% |
| webpage.html | web_asset | 173,857 | 11,194 | 6.4% |
| styles.css | web_asset | 262,144 | 43,321 | 16.5% |
| bundle.js | web_asset | 162,814 | 15,651 | 9.6% |

Each file is compressed at levels 1, 6, and 9 (raw DEFLATE, no zlib header).
Compressed files have suffix `.deflate.l{level}`.
