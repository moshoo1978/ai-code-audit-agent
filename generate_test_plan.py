import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 8))

# Draw Building Outer Boundary
rect_outer = patches.Rectangle((0, 0), 20, 15, fill=False, edgecolor='black', linewidth=3)
ax.add_patch(rect_outer)

# Draw Room 101 (Office)
rect_office = patches.Rectangle((0, 5), 10, 10, fill=False, edgecolor='blue', linewidth=2)
ax.add_patch(rect_office)
ax.text(2, 10, "OFFICE 101\nOccupancy: 15", fontsize=10, weight='bold')

# Draw Main Exit Corridor A (INTENTIONALLY FLAWED: 38 inches wide instead of 44 inches)
rect_corridor = patches.Rectangle((0, 0), 20, 3.16, fill=False, edgecolor='red', hatch='//') # 3.16 ft = 38 inches
ax.add_patch(rect_corridor)
ax.text(5, 1.5, "MAIN EXIT CORRIDOR A\nWidth: 38 INCHES", fontsize=10, color='red', weight='bold')

# Draw Exit Door
ax.plot([20, 20], [0, 3.16], color='green', linewidth=4)
ax.text(17.5, 3.5, "DOOR 101\nClear Width: 32 INCHES", fontsize=9, color='green')

# Formatting
ax.set_xlim(-2, 22)
ax.set_ylim(-2, 17)
ax.set_title("TEST DRAWING SHEET A-101: Floor Plan & Egress Layout", fontsize=14, weight='bold')
ax.grid(True, linestyle='--', alpha=0.5)

# Save to PDF
plt.savefig("sample_plan_A101.pdf", bbox_inches='tight')
print("✅ Test Floor Plan Generated: sample_plan_A101.pdf")
