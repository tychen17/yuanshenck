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

# 计算可抽取的命座数
def calculate_constellations(primo, crystal, padded_pulls, existing_pulls, desired_constellations):
    total_pulls_available = primo // PRIMO_TO_PULL + crystal // PRIMO_TO_PULL + existing_pulls
    constellations_obtained = min(total_pulls_available // padded_pulls, desired_constellations)
    remaining_pulls = total_pulls_available - constellations_obtained * padded_pulls
    return constellations_obtained, remaining_pulls

# 计算还需充值多少钱及充值档次选择
def calculate_recharge(primo, crystal, padded_pulls, existing_pulls, desired_constellations):
    constellations_obtained, _ = calculate_constellations(primo, crystal, padded_pulls, existing_pulls, desired_constellations)
    total_constellations_needed = desired_constellations - constellations_obtained
    pulls_needed = total_constellations_needed * padded_pulls
    primo_needed = pulls_needed * PRIMO_TO_PULL - primo - (crystal * PRIMO_TO_PULL)
    
    money_needed = 0
    recharge_plan = []

    for tier, price in sorted(RECHARGE_TIERS.items(), key=lambda item: item[1], reverse=True):
        while primo_needed >= tier:
            primo_needed -= tier
            money_needed += price
            recharge_plan.append(price)
    
    if primo_needed > 0:
        for tier, price in sorted(RECHARGE_TIERS.items(), key=lambda item: item[0], reverse=True):
            if primo_needed <= tier:
                money_needed += price
                recharge_plan.append(price)
                break

    return money_needed, recharge_plan

# 执行计算并显示结果
def calculate():
    try:
        primo = int(primo_entry.get())
        crystal = int(crystal_entry.get())
        padded_pulls = int(padded_pulls_entry.get())
        existing_pulls = int(existing_pulls_entry.get())
        desired_constellations = int(desired_constellations_entry.get())

        constellations_obtained, remaining_pulls = calculate_constellations(primo, crystal, padded_pulls, existing_pulls, desired_constellations)
        money_needed, recharge_plan = calculate_recharge(primo, crystal, padded_pulls, existing_pulls, desired_constellations)

        result_message = f"目前能抽出的命座数为：{constellations_obtained}\n" \
                         f"还需充值金额为：{money_needed}元\n" \
                         f"充值档次选择的最优解为：{recharge_plan}\n" \
                         f"还剩的抽取数为：{remaining_pulls}"
        messagebox.showinfo("抽卡规划结果", result_message)
    except ValueError:
        messagebox.showerror("错误", "请输入正确的数值！")

# 创建主窗口
root = tk.Tk()
root.title("原神抽卡规划程序")

# 创建输入框标签和输入框
tk.Label(root, text="原石数量").grid(row=0, column=0)
primo_entry = tk.Entry(root)
primo_entry.grid(row=0, column=1)

tk.Label(root, text="结晶数量").grid(row=1, column=0)
crystal_entry = tk.Entry(root)
crystal_entry.grid(row=1, column=1)

tk.Label(root, text="垫的抽数（大保底）").grid(row=2, column=0)
padded_pulls_entry = tk.Entry(root)
padded_pulls_entry.grid(row=2, column=1)

tk.Label(root, text="已有抽数").grid(row=3, column=0)
existing_pulls_entry = tk.Entry(root)
existing_pulls_entry.grid(row=3, column=1)

tk.Label(root, text="需要命座").grid(row=4, column=0)
desired_constellations_entry = tk.Entry(root)
desired_constellations_entry.grid(row=4, column=1)

# 创建计算按钮
calculate_button = tk.Button(root, text="计算", command=calculate)
calculate_button.grid(row=5, columnspan=2)

# 运行主循环
root.mainloop()

