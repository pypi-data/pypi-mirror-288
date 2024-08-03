# import torch

# def lowpass_filter(exg, exg_frequency, cutoff_frequency, order=3):
#     fexg = torch.fft.fft(exg)
#     fexg = torch.fft.fftshift(fexg)

#     range = torch.linspace(-0.5*exg.shape[-1], 0.5*exg.shape[-1]-1, steps=exg.shape[-1]).abs() / cutoff_frequency

#     gexg = fexg / (1 + range**order)
#     gexg = torch.fft.ifftshift(gexg)
#     exg = torch.fft.ifft(gexg).real

#     return exg
