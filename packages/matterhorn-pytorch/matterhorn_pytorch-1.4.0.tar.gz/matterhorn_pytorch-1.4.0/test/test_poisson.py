import torch
import matterhorn_pytorch.snn as snn

def main():
    r = 0.99 + 0.01 * torch.rand(2, 3)
    print(r)
    p = snn.PoissonEncoder(
        time_steps = 8,
        spike_mode = "m"
    ).multi_step_mode_()
    s = p(r)
    print(s)

if __name__ == "__main__":
    main()