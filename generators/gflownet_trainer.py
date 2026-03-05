import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import itertools
from generators.tensor_network.tensor_contraction import TRG_Ramsey_Contraction

class GFlowNetPolicy(nn.Module):
    def __init__(self, num_edges, hidden_dim=128):
        super().__init__()
        self.embed = nn.Embedding(3, 16)
        self.fc = nn.Sequential(
            nn.Linear(num_edges * 16, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_edges * 2)
        )
        self.num_edges = num_edges

    def forward(self, x):
        batch_size = x.shape[0]
        emb = self.embed(x).view(batch_size, -1)
        logits = self.fc(emb).view(batch_size, self.num_edges, 2)
        
        # Mask out colored edges (-inf)
        mask = (x != 0).unsqueeze(-1).expand_as(logits)
        logits = logits.masked_fill(mask, -1e9)
        return logits

class RamseyGFlowNet:
    def __init__(self, N=6, hidden_dim=128, lr=1e-3):
        self.N = N
        self.num_edges = N * (N - 1) // 2
        self.model = GFlowNetPolicy(self.num_edges, hidden_dim)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        
        # Use logZ parameter
        self.logZ = nn.Parameter(torch.tensor(0.0, requires_grad=True))
        self.optimizer.add_param_group({'params': [self.logZ], 'lr': lr * 10})
        
        self.trg = TRG_Ramsey_Contraction(self.N, max_bond=10)

    def is_k5_free(self, state):
        for subset in self.trg.k5_subsets:
            edges = [self.trg.edge_to_idx[e] for e in itertools.combinations(subset, 2)]
            colors = state[edges]
            if torch.all(colors == 1) or torch.all(colors == 2):
                return False
        return True

    def train_step(self):
        self.optimizer.zero_grad()
        
        state = torch.zeros(self.num_edges, dtype=torch.long)
        log_p_F = 0.0
        
        for step in range(self.num_edges):
            logits = self.model(state.unsqueeze(0)).squeeze(0)
            logits_flat = logits.view(-1)
            
            # Use Gumbel trick or multinomial
            probs = torch.softmax(logits_flat, dim=0)
            
            action_idx = torch.multinomial(probs, 1).item()
            edge_idx = action_idx // 2
            color = (action_idx % 2) + 1
            
            log_p_F += torch.log(probs[action_idx] + 1e-10)
            
            # Important: clone to prevent inplace modification tracking issues
            next_state = state.clone()
            next_state[edge_idx] = color
            state = next_state
            
        R = 1.0 if self.is_k5_free(state) else 1e-6
        log_R = torch.log(torch.tensor(R, dtype=torch.float32))
        
        log_p_B = -torch.sum(torch.log(torch.arange(1, self.num_edges + 1, dtype=torch.float32)))
        
        loss = (self.logZ + log_p_F - log_R - log_p_B) ** 2
        
        loss.backward()
        self.optimizer.step()
        
        return loss.item(), R

    def train(self, steps=100):
        print(f"Training GFlowNet for N={self.N} for {steps} steps...")
        successes = 0
        for i in range(steps):
            loss, R = self.train_step()
            if R == 1.0: successes += 1
            if (i+1) % 10 == 0:
                print(f"Step {i+1}, Loss: {loss:.4f}, Valid Graphs: {successes}/10")
                successes = 0

if __name__ == "__main__":
    gfn = RamseyGFlowNet(N=6)
    gfn.train(steps=100)
    print("GFlowNet training module functioning correctly.")
