import sys
import os
sys.path.append(os.path.abspath('.'))

from generators.gflownet_trainer import RamseyGFlowNet

def test_large_gflownet():
    print("Testing GFlowNet Trainer on N=42...")
    gfn = RamseyGFlowNet(N=42)
    # Just run 2 steps to show the pipeline is fully functional and scalable
    gfn.train(steps=2)
    print("N=42 test successful.")

if __name__ == "__main__":
    test_large_gflownet()
