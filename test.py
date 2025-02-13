class Solution:
    def BinarySort(self, array):
        for i in range(1, len(array)):
            key = array[i]
            j = i - 1
            while j >= 0 and key < array[j]:
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = key
        return array[0]


if __name__ == "__main__":
    nums = [1, 2, 3, 4, 5, 6, 9, 8, 123]
    target = 5
    print(Solution().BinarySort(nums))
