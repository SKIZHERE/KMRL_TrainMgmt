def score_trainset(trainset):
    score = 0
    reasons = []

    # 1. Fitness certificate
    if trainset.get("fitness") == "valid":
        score += 30
        reasons.append("Fitness OK")
    else:
        reasons.append("Fitness expired")

    # 2. Job-card
    if trainset.get("jobcard") == "closed":
        score += 20
        reasons.append("Jobcard closed")
    else:
        reasons.append("Pending jobcard")

    # 3. Branding priority
    if trainset.get("branding") == "priority":
        score += 10
        reasons.append("Branding priority")

    return score, reasons
