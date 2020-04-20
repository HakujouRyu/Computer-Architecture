dic = {
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}

total = 0
for item in dic.values():
    if type(item) == int:
        total += item


print(total)