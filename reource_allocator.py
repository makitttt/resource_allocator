input_instances = {"us-east":{
                    "large":0.12,
                    "xlarge":0.23,
                    "2xlarge":0.45,
                    "4xlarge":0.774,
                    "8xlarge":1.4,
                    "10xlarge":2.82},
                   "us-west":{
                     "large":0.14,
                     "2xlarge":0.413,
                     "4xlarge":0.89,
                     "8xlarge":1.3,
                     "10xlarge":2.97},
                     "asia":{
                         "large":0.11,
                         "xlarge":0.20,
                         "4xlarge":0.67,
                         "8xlarge":1.18
                     }}


server_list_map = ["large","xlarge","2xlarge","4xlarge","8xlarge","10xlarge"]



def serverWithCpuPrice(no_cpu,sum_li,server_list,cost_list,max_price):
    i           = len(server_list)
    ans         = [0 for q in range(i)]
    cost_margin = [0 for p in range(i)]
    while sum(cost_margin) <= max_price :					
        if no_cpu > sum_li :	
            if(sum(cost_list[0:i]) <= max_price):				
                if sum_li > 0:
                    incr   = no_cpu // sum_li
                    no_cpu = no_cpu % sum_li
                else:
                    ans[0] = ans[0] + 1
                    break
                for x in range(i):
                    if server_list[x] > 0 :							
                        ans[x] += incr
                    else:
                        ans[x] = 0
                cost_margin = [a*b for a,b in zip(ans,cost_list)]
                if sum(cost_margin) > max_price:
                    for x in range(i):
                        if server_list[x] > 0 :				
                            ans[x] -= incr
                    sum_li = sum_li - server_list[i-1]
                    i = i - 1
                                        
            else:
                if server_list[i-1] > 0:
                    sum_li = sum_li - server_list[i-1]
                i = i -1
        else:
            if server_list[i-1] > 0:
                sum_li = sum_li - server_list[i-1]
            i = i -1
            
    return ans
  
def serverWithPrice(no_cpu,sum_li,server_list):

    i   = len(server_list)
    ans = [0 for q in range(i)]
    while i >= 0 :
        if no_cpu > sum_li :
            if sum_li > 0:
                incr = no_cpu//sum_li
                no_cpu = no_cpu % sum_li
            else :
                ans[0] = ans[0] + 1
                break
            for x in range(i):
                if server_list[x] > 0:
                    ans[x] += incr
                else:
                    ans[x] = 0
        else :
            if server_list[i-1] > 0:
                sum_li = sum_li - server_list[i-1]
            i = i - 1
    return ans
    
def serverWithNoCPU(price,cost_list,server_list):
    i         = len(cost_list)
    ans       = [0 for val in range(i)]
    cost      = 0
    rem_price = price
    while i >= 0:
        if cost_list[i-1] < 0:
            i = i-1
        elif cost_list[i-1] <= rem_price:
            rem_price = rem_price - cost_list[i-1]
            if server_list[i-1] > 0:
                ans[i-1] = ans[i-1] + 1
        else:
            i = i-1
    return ans

def getServerCombination(server_combination_t,total_cost,cost_list_h,server_combination):

    server_combination_t = [float(val) for val in server_combination_t]
    
    total_cost.append([a*b for a,b in zip(server_combination_t,cost_list_h)])
    
    server_combination_t = [int(val) for val in server_combination_t]

    server_combination.append(server_combination_t)

    return server_combination,total_cost

def setupServerCostList(server_list_map,hours,cpus,price):
    server_combination_t = []
    server_combination   = []
    total_cost           = []
    for k,v in input_instances.items():

        server_list = [0 for s in range(len(server_list_map))]

        cost_list = [0 for s in range(len(server_list_map))]
        
        for i in range(len(server_list_map)):
            if server_list_map[i] in list(v.keys()):
                server_list[i] = 2**i
                cost_list[i]   = v[server_list_map[i]]
            else:
                cost_list[i]   = -1
        
        cost_list_h = [h*hours for h in cost_list]

        sum_server_list = sum(server_list)
        
        if price == 0.0:
            server_combination_t = serverWithPrice(cpus,sum_server_list,server_list)
        
        elif cpus == 0:
            server_combination_t = serverWithNoCPU(price,cost_list_h,server_list)

        else:
            server_combination_t = serverWithCpuPrice(cpus,sum_server_list,server_list,cost_list_h,price)
        
        retServerList,retTotalCost = getServerCombination(server_combination_t, total_cost, cost_list_h, server_combination)
    
    return retTotalCost,retServerList       
        

def get_costs(hours,cpus,price):
    
    cost_list = []
    ans_list  = []
    #Few error handling statementss
    if hours is None or hours < 0:
        print("Invalid input (hour)")
        return
    elif price < 0.0:
        print ("Invalid input (price)")
        return
    elif cpus < 0:
        print ("Invalid input (cpus)")
        return
    else:
        totalCost,retServers = setupServerCostList(server_list_map,hours,cpus,price)
        flag = 0
        
        for i in range(len(totalCost)):
            cost_list.append(sum(totalCost[i]))
        
        for k in input_instances.keys():
            ans_dict = {}
            if flag == 0:
                counter = 0
                flag    = 1
            else:
                counter += 1
            ans_dict["region"] = k

            ans_dict["total_cost"] = cost_list[counter]
            
            ans_dict["servers"] = []
            
            for s in range(len(server_list_map)):
                if retServers[counter][s] > 0.0:
                    sr = (server_list_map[s],retServers[counter][s])
                    ans_dict["servers"].append(sr)
            ans_list.append(ans_dict)

        ans_list = sorted(ans_list, key = lambda i:i["total_cost"])
    
    return ans_list