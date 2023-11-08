import tkinter as tk
from tkinter import messagebox

# 充值档次及对应的结晶数量（中国区）
RECHARGE_TIERS = {
    8080: 648,
    3880: 328,
    2240: 198,
    1090: 98,
    330: 30,
    60: 6
}

# 原石和结晶兑换抽数的比例
PRIMO_TO_PULL = 160  # 160原石兑换一次抽卡

# 大保底的抽数
MAX_PITY = 160

# 抽卡的价格（人民币），每次抽卡按照最小充值档次计算
PRICE_PER_PULL = min(RECHARGE_TIERS.keys())

# 计算所需的原石数量
def calculate_primos_needed(desired_constellations, desired_pulls, existing_pulls, padded_pulls):
    if desired_constellations > 0:
        # 如果设定了需要的命座数
        total_pulls_needed = desired_constellations * MAX_PITY
    elif desired_pulls > 0:
        # 如果设定了期望的抽数
        total_pulls_needed = desired_pulls
    else:
        return None, "请输入需要的命座数或期望抽数。"
    
    pulls_remaining_after_existing = max(total_pulls_needed - existing_pulls - padded_pulls, 0)
    primos_needed = pulls_remaining_after_existing * PRIMO_TO_PULL
    return primos_needed, ""

# 计算充值方案
def find_best_recharge_plan(primos_needed):
    sorted_tiers = sorted(RECHARGE_TIERS.items(), key=lambda item: item[1], reverse=True)
    recharge_plan = []
    for primo, cost in sorted_tiers:
        while primos_needed >= primo:
            primos_needed -= primo
            recharge_plan.append(cost)
    if primos_needed > 0:
        # 如果还有剩余，就选择下一个最小的档次
        for primo, cost in sorted(RECHARGE_TIERS.items(), key=lambda item: item[0]):
            if primos_needed > 0:
                primos_needed -= primo
                recharge_plan.append(cost)
                break
    total_cost = sum(recharge_plan)
    return recharge_plan, total_cost

# 执行计算并显示结果
def calculate():
    try:
        primo = int(primo_entry.get())
        crystal = int(crystal_entry.get())
        padded_pulls = int(padded_pulls_entry.get())
        existing_pulls = int(existing_pulls_entry.get())
        desired_constellations = int(desired_constellations_entry.get())
        desired_pulls = int(desired_pulls_entry.get())

        # 计算所需原石
        primos_needed, message = calculate_primos_needed(desired_constellations, desired_pulls, existing_pulls, padded_pulls)
        if message:
            messagebox.showerror("错误", message)
            return

        # 减去用户已有的原石和结晶
        primos_needed -= (primo + crystal * PRIMO_TO_PULL)

        # 计算充值方案
        recharge_plan, total_cost = find_best_recharge_plan(primos_needed)

        result_message = f"总计需要充值金额为：{total_cost}元\n" \
                         f"充值档次选择的最优解为：{recharge_plan}\n" \
                         f"总计需要抽数为：{desired_pulls}\n" \
                         f"总计需要命座数为：{desired_constellations}"

        messagebox.showinfo("抽卡规划结果", result_message)

    except ValueError:
        messagebox.showerror("错误", "请输入正确的数值！")

# GUI布局和运行主循环的部分与您提供的相同
