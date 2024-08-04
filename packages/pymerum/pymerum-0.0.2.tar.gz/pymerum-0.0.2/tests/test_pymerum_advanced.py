# -*- coding: utf-8 -*-
import pytest
import pymerum

original_text = (
    "ᱥᱟᱱᱛᱟᱞ ᱦᱳᱨᱠᱩᱰᱟᱴᱟ ᱯᱟᱨᱞᱟᱢᱮᱱᱛᱨᱮᱟᱞᱳᱟᱠᱟᱱᱞᱮᱠᱟᱛᱮᱵᱟᱱᱪᱦᱟᱳᱟᱠᱟᱱᱦᱳᱨᱠᱳᱦᱚᱛᱮᱛᱮᱠᱟᱢᱤ、ᱟᱵᱚᱟᱨᱟᱵᱚᱨᱮᱱ"
    "ᱜᱤᱰᱨᱟᱠᱳᱞᱟᱜᱤᱛ"
)

expected = [
    {
        "orig": "ᱥᱟᱱᱛᱟᱞ ᱦᱳᱨᱠᱩ",
        "hor": "ᱥᱟᱱᱛᱟᱞ ᱦᱳᱨᱠᱩ",
        "hura": "ᱥᱟᱱᱛᱟᱞ ᱦᱳᱨᱠᱩ",
        "marburu": "santal horku",
        "kunrei": "santal horku",
        "passport": "santar horku",
    },
    {
        "orig": "ᱰᱟᱴᱟ",
        "hor": "ᱰᱟᱴᱟ",
        "hura": "ᱰᱟᱴᱟ",
        "marburu": "data,",
        "kunrei": "data",
        "passport": "data",
    },
    {
        "orig": "ᱯᱟᱨᱞᱟᱢᱮᱱᱛ",
        "hor": "ᱯᱟᱨᱞᱟᱢᱮᱱᱛ",
        "hura": "ᱯᱟᱨᱞᱟᱢᱮᱱᱛ",
        "marburu": "Parliament",
        "kunrei": "Parliament",
        "passport": "Parliament",
    },
    # Add the remaining expected entries here...
]

def test_merum_structured_constitution():
    merum = pymerum.mamerum()
    result = merum.convert(original_text)
    for i, e in enumerate(expected):
        print(f"Testing item {i + 1}")
        print(f"Expected: {e}")
        print(f"Result: {result[i]}")
        
        assert result[i]["orig"] == e["orig"], f"Mismatch in orig: {result[i]['orig']} != {e['orig']}"
        assert result[i]["hura"] == e["hura"], f"Mismatch in hura: {result[i]['hura']} != {e['hura']}"
        assert result[i]["hor"] == e["hor"], f"Mismatch in hor: {result[i]['hor']} != {e['hor']}"
        assert result[i]["marburu"] == e["marburu"], f"Mismatch in marburu: {result[i]['marburu']} != {e['marburu']}"
        assert result[i]["kunrei"] == e["kunrei"], f"Mismatch in kunrei: {result[i]['kunrei']} != {e['kunrei']}"
        assert result[i]["passport"] == e["passport"], f"Mismatch in passport: {result[i]['passport']} != {e['passport']}"

@pytest.mark.benchmark
def test_benchmark(benchmark):
    merum = pymerum.mamerum()
    benchmark.extra_info["data_size"] = len(original_text)
    
    # Run benchmark and print results
    result = benchmark(merum.convert, original_text)
    
    print("Benchmark results:")
    print(f"Data Size: {benchmark.extra_info['data_size']} characters")
    print(f"Result for first item in expected: {result[0]}")
    
    assert result[0]["hura"] == expected[0]["hura"], f"Benchmark mismatch in hura: {result[0]['hura']} != {expected[0]['hura']}"
