def percentage_difference(a, b):
  """
  Calculates the percentage difference between two numbers.

  Args:
    a: The first number.
    b: The second number.

  Returns:
    The percentage difference between the two numbers.
  """

  difference = b - a
  percentage = difference / a * 100
  return percentage


def main():
  """
  Calculates the addition of the percentages of the difference of 420 and 560 and 560 and 650.

  Returns:
    The addition of the percentages of the difference.
  """

  percentage_1 = percentage_difference(420, 560)
  percentage_2 = percentage_difference(560, 650)
  addition = percentage_1 + percentage_2
  return addition


if __name__ == "__main__":
  print(main())
