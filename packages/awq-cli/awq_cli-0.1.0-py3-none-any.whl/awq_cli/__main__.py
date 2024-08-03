"""
Command-line interface for AutoAWQ.
"""

import argparse

from . import quantize, inference


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="awq-cli",
        description="Command-line interface for AutoAWQ.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        metavar="DEVICE",
        help="Device for loading the model",
    )
    parser.add_argument(
        "--trust-remote-code",
        action="store_true",
        help="Allow custom models",
    )
    parser.add_argument(
        "--use-cache",
        action="store_true",
        help="Use cache while loading",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create parser for the "quantize" command.
    parser_quantize = subparsers.add_parser(
        name="quantize",
        help="Quantize and export model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_quantize.add_argument(
        "model",
        type=str,
        help="Name or path of the model to be quantized",
    )
    parser_quantize.add_argument(
        "-o",
        "--output",
        type=str,
        default="model_quantized",
        metavar="PATH",
        help="Path to save the quantized model",
    )
    parser_quantize.add_argument(
        "-d",
        "--calibration-dataset",
        type=str,
        metavar="PATH",
        help="Path to the calibration dataset",
    )
    parser_quantize.add_argument(
        "--calibration-parallel",
        type=int,
        default=None,
        metavar="N",
        help="Number of parallel samples to run through the model",
    )
    parser_quantize.add_argument(
        "--calibration-max-samples",
        type=int,
        default=128,
        metavar="N",
        help="Maximum number of samples to run through the model",
    )
    parser_quantize.add_argument(
        "--calibration-max-length",
        type=int,
        default=512,
        metavar="LEN",
        help="Maximum sequence length of the calibration dataset",
    )
    parser_quantize.add_argument(
        "-s",
        "--shard-size",
        type=str,
        default="4GB",
        metavar="SIZE",
        help="Shard size for saving the quantized model",
    )
    parser_quantize.add_argument(
        "-b",
        "--bit-rate",
        type=int,
        default=4,
        metavar="BIT",
        help="Quantization bit rate",
    )
    parser_quantize.add_argument(
        "-g",
        "--group-size",
        type=int,
        default=128,
        metavar="SIZE",
        help="Quantization group size",
    )
    parser_quantize.add_argument(
        "-m",
        "--multiplication",
        type=str,
        default="GEMM",
        metavar="VERSION",
        help="Version of matrix multiplication",
    )
    parser_quantize.add_argument(
        "--disable-zero-point",
        action="store_true",
        help="Disable zero point quantization",
    )

    # Create parser for the "inference" command.
    parser_inference = subparsers.add_parser(
        name="inference",
        help="Run quantized model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_inference.add_argument(
        "model",
        type=str,
        help="Name or path of the model to be served",
    )
    parser_inference.add_argument(
        "--fuse-layers",
        action="store_true",
        help="Combine multiple layers into a single operation",
    )

    return parser.parse_args()


def main():
    """Command-line interface for AutoAWQ."""
    args = parse_args()
    if args.command == "quantize":
        quantize(
            model=args.model,
            output=args.output,
            calibration_dataset=args.calibration_dataset,
            calibration_parallel=args.calibration_parallel,
            calibration_max_samples=args.calibration_max_samples,
            calibration_max_length=args.calibration_max_length,
            shard_size=args.shard_size,
            bit_rate=args.bit_rate,
            group_size=args.group_size,
            multiplication=args.multiplication,
            disable_zero_point=args.disable_zero_point,
            device=args.device,
            trust_remote_code=args.trust_remote_code,
            use_cache=args.use_cache,
        )
    elif args.command == "inference":
        inference()
    else:
        raise ValueError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    main()
