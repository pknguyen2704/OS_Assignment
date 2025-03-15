#Banker Algorithm

#Define nums of process and resources
num_process = 0
num_resources = 0

def isDeadlock(request, allocation):
    finish = [0] * num_process
    work = [0] * num_resources
    count = 0
    safeSeq = []
    while(count < num_process):
        found = False
        for i in range(num_process):
            if (finish[i] == False):
                for j in range(num_resources):
                    if(request[i][j] > work[j]):
                        break
                if(j == num_resources-1):
                    for j in range(num_resources):
                        work[j] += allocation[i][j]
                    found = True
                    finish[i] = True                    
                    safeSeq.append(i)
        if(found == False):
            if(not all(finish)):
                return True
            else:
                print(f"Chuỗi {safeSeq} cho phép Finish[i] = true với tất cả 0 ≤ i ≤ n-1")
                break
    return False


def calculateNeedMatrix(allocation, maxm, need):
    for i in range(num_process):
        for j in range(num_resources):
            need[i][j] = maxm[i][j] - allocation[i][j]


def isSafe(allocation, maxm, available):
    need = []
    for i in range(num_process):
        l = []
        for j in range(num_resources):
            l.append(0)
        need.append(l)
    
    calculateNeedMatrix(allocation, maxm, need)
    safeSeq = []
    finish = [0] * num_process
    work = [0] * num_resources
    for i in range(num_resources):
        work[i] = available[i]
    
    while(True):
        found = False
        for i in range(num_process):
            if(finish[i] == 0):
                for j in range(num_resources):
                    if(need[i][j] > work[j]):
                        break
                if (j == num_resources - 1):
                    for j in range(num_resources):
                        work[j] += allocation[i][j]
                    finish[i] = True
                    found = True
                    safeSeq.append(i)
        if(found == False):
            return False
        if(all(finish)):
            break
    
    return safeSeq

def isRequestValid(request, proceed_id, need, allocation):
    for j in range(num_resources):
        if(request[j] > need[proceed_id][j] or request[j] > available[j]):
            return False
    return True

def requestResource(request, process_id, available, allocation):
    need = []
    for i in range(num_process):
        l = []
        for j in range(num_resources):
            l.append(0)
        need.append(l)
    calculateNeedMatrix(allocation, maxm, need)

    if(isRequestValid(request, process_id, need, allocation) == False):
        return (f"Kết quả yêu cầu của tiến trình {process_id} không hợp lệ")
    else:
        for j in range(num_resources):
            available[j] -= request[j]
            allocation[process_id][j] += request[j]
            need[process_id][j] -= request[j]
        if(isSafe(allocation, maxm, available)):
            return (f"Kết quả yêu cầu của tiến trình {process_id} được cấp phát")
        else:
            for j in range(num_resources):
                available[j] += request[j]
                allocation[process_id][j] -= request[j]
                need[process_id][j] += request[j]
            return (f"Kết quả yêu cầu của tiến trình {process_id} bị từ chối")
        

if __name__ == "__main__":
    process = [0, 1, 2, 3, 4]
    num_process = len(process)
    num_resources = 3

    need = []
    for i in range(num_process):
        l = []
        for j in range(num_resources):
            l.append(0)
        need.append(l)

    print(num_process, num_resources)
    allocation = [[0,1,0], [2,0,0], [3,0,2], [2,1,1], [0,0,2]]
    request = [[0, 0, 0], [2,0,2], [0,0,1], [1,0,0], [0,0,2]]
    maxm = [[7,5,3], [3,2,2], [9,0,2], [2,2,2], [4,3,3]]
    available = [3, 3, 2]

    # request_1 = [1, 0, 2]
    # print(requestResource(request_1, 1, available, allocation))
    # print(allocation)

    # request_4 = [3,3,0]
    # print(requestResource(request_4, 4, available, allocation))
    # print(allocation)
    # print(available)

    # request_0 = [0,2,0]
    # print(requestResource(request_0, 0, available, allocation))
    # print(allocation)
    # print(available)

    if(isDeadlock(request, allocation)):
        print("Hệ thống bị bế tắc")
    else:
        print("Hệ thống không bị bế tắc ")
    # safeSeq = isSafe(allocation, maxm, available)
    # if(safeSeq):
    #     print("Hệ thống hiện tại an toàn, Thứ tự an toàn: ", safeSeq)
    # else:
    #     print("Hệ thống hiện tại không an toàn")
