
with open("input.txt", "r") as f:
    inventories = [[int(calorie) for calorie in inventory.split("\n") if calorie.split()] for inventory in f.read().split("\n\n") if inventory.split()]

print(inventories)
calories_total = [sum(inventory) for inventory in inventories]
print(max(calories_total))
# Part 2
calories_total.sort()
print(sum(calories_total[-3:]))
