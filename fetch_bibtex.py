import subprocess
ids = [
    "65b977acda019f0ad48d5b7c0b4ca1e21cc8c180",
    "ce58c8371aa282534fd507f805cb27f77c339467",
    "533d6d4f8759f228c191dc21786322b92e192d54",
    "626750990975e3324753cd943e52d1a854e97459",
    "a203bd181d2134069f96517ea8e968317317adf0",
    "160081e3e1f57e3478499da04264f84564db90f2",
    "15b38042fd03d5b8204825ac1de5231d546d5466",
    "6c98207a47cd3589e71665543b42bb188a0b0ce3",
    "f9d2aa2e1345d26734ab530fa006abd194724948",
    "b3fd26ca357555248faf8ad4315031c10234fad8",
    "b9beb333022149e69d89f711033547d4d65a8277"
]

with open("sources.bib", "a") as f:
    for i in ids:
        try:
            res = subprocess.run(["python3", ".archivara/semantic_scholar.py", "bibtex", i], capture_output=True, text=True, timeout=30)
            f.write(res.stdout + "\n")
        except Exception as e:
            print("Failed", i, e)
