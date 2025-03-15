class BankerAlgorithm:
    def __init__(self, max_resources, allocation, available):
        self.max_resources = max_resources  # Max allocation matrix
        self.allocation = allocation  # Allocation matrix
        self.available = available  # Available resources
        self.num_processes = len(max_resources)
        self.num_resources = len(available)
        self.need = [[0] * self.num_resources for _ in range(self.num_processes)]
        self.calculate_need_matrix()

    def calculate_need_matrix(self):
        for i in range(self.num_processes):
            for j in range(self.num_resources):
                self.need[i][j] = self.max_resources[i][j] - self.allocation[i][j]

    def request_resources(self, process_id, request):
        if self.is_request_valid(process_id, request):
            for j in range(self.num_resources):
                self.available[j] -= request[j]
                self.allocation[process_id][j] += request[j]
                self.need[process_id][j] -= request[j]

            if self.is_safe():
                return "Yêu cầu được cấp phát"
            else:
                # Hoàn tác phân bổ tài nguyên nếu không tìm thấy phân bổ an toàn
                for j in range(self.num_resources):
                    self.available[j] += request[j]
                    self.allocation[process_id][j] -= request[j]
                    self.need[process_id][j] += request[j]
                return "Yêu cầu bị từ chối"
        else:
            return "Yêu cầu không hợp lệ"

    def is_request_valid(self, process_id, request):
        for j in range(self.num_resources):
            if (
                request[j] > self.need[process_id][j]
                or request[j] > self.available[j]
            ):
                return False
        return True

    def is_safe(self):
        work = self.available[:]
        finish = [False] * self.num_processes
        safe_sequence = []

        while True:
            safe_found = False
            for i in range(self.num_processes):
                if not finish[i] and all(
                    self.need[i][j] <= work[j]
                    for j in range(self.num_resources)
                ):
                    for j in range(self.num_resources):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    safe_found = True
                    safe_sequence.append(i)

            if not safe_found:
                return False

            if all(finish):
                return safe_sequence

# Ví dụ minh họa sử dụng thuật toán Banker
max_resources = [
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2],
    [2, 2, 2],
    [4, 3, 3],
]
allocation = [
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2],
]
available = [3, 3, 2]

banker = BankerAlgorithm(max_resources, allocation, available)

# # Yêu cầu tài nguyên cho tiến trình 1
# request_1 = [1, 0, 2]
# result_1 = banker.request_resources(1, request_1)
# print("Kết quả yêu cầu cho tiến trình 1:", result_1)

# Yêu cầu tài nguyên cho tiến trình 4
request_4 = [3, 3, 0]
result_4 = banker.request_resources(4, request_4)
print("Kết quả yêu cầu cho tiến trình 4:", result_4)

# Kiểm tra tính an toàn
# safe_sequence = banker.is_safe()
# if safe_sequence:
#     print("Hệ thống hiện tại an toàn, Thứ tự an toàn:", safe_sequence)
# else:
#     print("Hệ thống hiện tại không an toàn")