import torch


class ToTensorWithoutScaling(object):

    def __call__(self, np_img):
        return torch.from_numpy(np_img).permute(2, 0, 1).float()


class TensorCenterCrop(object):

    def __init__(self, crop_size: int) -> None:
        self.crop_size = crop_size

    def __call__(self, tensor: torch.FloatTensor) -> torch.FloatTensor:
        H, W = tensor.size(-2), tensor.size(-1)
        from_H = ((H - self.crop_size) // 2)
        from_W = ((W - self.crop_size) // 2)
        to_H = from_H + self.crop_size
        to_W = from_W + self.crop_size
        return tensor[..., from_H:to_H, from_W:to_W]


class ScaleTo1_1(object):

    def __call__(self, tensor: torch.FloatTensor) -> torch.FloatTensor:
        return (2 * tensor / 255) - 1


class PermuteAndUnsqueeze(object):

    def __call__(self, tensor: torch.FloatTensor) -> torch.FloatTensor:
        return tensor.permute(1, 0, 2, 3).unsqueeze(0)


class Clamp(object):

    def __init__(self, min_val, max_val) -> None:
        self.min_val = min_val
        self.max_val = max_val

    def __call__(self, tensor):
        return torch.clamp(tensor, min=self.min_val, max=self.max_val)


class ToUInt8(object):

    def __call__(self, flow_tensor: torch.FloatTensor) -> torch.FloatTensor:
        # preprocessing as in
        # https://github.com/deepmind/kinetics-i3d/issues/61#issuecomment-506727158
        # but for pytorch
        # [-20, 20] -> [0, 255]
        flow_tensor = 128 + 255 / 40 * flow_tensor
        return flow_tensor.round()


class ToChannelFirstToFloat(object):

    def __call__(self, tensor_fhwc: torch.Tensor) -> torch.Tensor:
        return tensor_fhwc.permute(3, 0, 1, 2).float()
