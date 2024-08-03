"""
Model quantization with AutoAWQ.
"""

import json
from typing import Generator, Optional

from transformers import AutoTokenizer
from awq import AutoAWQForCausalLM


def load_calibration_dataset(
    tokenizer: AutoTokenizer, path: str
) -> Generator[str, None, None]:
    """Load calibration dataset from JSONL file."""
    # The calibration dataset should be a JSONL file with one example per line:
    # https://platform.openai.com/docs/guides/fine-tuning/example-format
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            example = json.loads(line)
            text = tokenizer.apply_chat_template(
                example["messages"],
                tokenize=False,
                add_generation_prompt=False,
            )
            yield text.strip()


def quantize(
    model_path: str,
    output: str = "model_quantized",
    calibration_dataset: Optional[str] = None,
    calibration_parallel: Optional[int] = None,
    calibration_max_samples: int = 128,
    calibration_max_length: int = 512,
    shard_size: str = "4GB",
    bit_rate: int = 4,
    group_size: int = 128,
    multiplication: str = "GEMM",
    disable_zero_point: bool = False,
    device: str = "auto",
    trust_remote_code: bool = False,
    use_cache: bool = False,
):
    """Model quantization with AutoAWQ."""
    model = AutoAWQForCausalLM.from_pretrained(
        model_path,
        device_map=device,
        trust_remote_code=trust_remote_code,
        low_cpu_mem_usage=True,
        use_cache=use_cache,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=trust_remote_code,
    )

    # Load calibration dataset if specified.
    if calibration_dataset:
        print(f"Loading calibration dataset from: {calibration_dataset}")
        dataset = list(load_calibration_dataset(tokenizer, calibration_dataset))
    else:
        dataset = "pileval"

    # Quantize the model with AutoAWQ.
    model.quantize(
        tokenizer,
        quant_config={
            "w_bit": bit_rate,
            "q_group_size": group_size,
            "version": multiplication,
            "zero_point": not disable_zero_point,
        },
        calib_data=dataset,
        n_parallel_calib_samples=calibration_parallel,
        max_calib_samples=calibration_max_samples,
        max_calib_seq_len=calibration_max_length,
    )

    # Save the quantized model.
    model.save_quantized(output, shard_size=shard_size)
    tokenizer.save_pretrained(output)
    print(f"Model is quantized and saved to: {output}")
