from rag import retrieve_chunks

test_questions = [
    {
        "question": "كم مدة العقد؟",
        "expected_keywords": ["سنة", "سنتين", "مدة"]
    },
    {
        "question": "عدد ساعات العمل",
        "expected_keywords": ["8", "٨", "ساعات"]
    }
]

def run_benchmark():
    results = []

    for test in test_questions:
        chunks = retrieve_chunks(test["question"], top_k=2)
        combined = " ".join(chunks)

        keywords = test["expected_keywords"]

        if any(k in combined for k in keywords):
            score = 1
        else:
            score = 0

        results.append({
            "question": test["question"],
            "score": score
        })

    accuracy = sum(r["score"] for r in results) / len(results)

    return {
        "accuracy": accuracy,
        "details": results
    }


if __name__ == "__main__":
    print(run_benchmark())