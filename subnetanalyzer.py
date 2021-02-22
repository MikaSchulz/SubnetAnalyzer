ipRange = range(0, 32)


def full_adder(inputA, inputB, inputC):
    outputSum = inputA ^ (inputB ^ inputC)
    outputCarry = ((inputA ^ inputB) & inputC) | (inputA & inputB)
    return outputSum, outputCarry


def valid_ip(ip_address):
    if ip_address is None:
        return False
    ip_address_split = ip_address.split(".")
    if len(ip_address_split) != 4:
        return False
    for x in ip_address_split:
        if not x.isdigit():
            return False
        y = int(x)
        if y > 255 or y < 0:
            return False
    return True


def valid_cidr(cidr):
    if cidr is None:
        return False
    if not cidr.isdigit():
        return False
    y = int(cidr)
    if y < 0 or y > 32:
        return False
    return True


def conv_dec_to_same_bin_bit(first, second):
    if abs(first) < abs(second):
        temp = first
        first = second
        second = temp
    first_result = dec_to_bin(first, 0, True)
    second_result = dec_to_bin(second, len(first_result) - 1, True)
    return first_result, second_result


def calc(first_string, second_string):
    first = list(map(int, first_string))
    second = list(map(int, second_string))
    summ = ""
    x = len(first) - 1
    tempSum = 0
    carry = 0
    while x >= 0:
        # print(first[x], second[x], carry)
        tempSum, carry = full_adder(first[x], second[x], carry)
        # print(tempSum, carry)
        summ += str(tempSum)
        x -= 1
    # print(first[0], second[0], carry)
    sumExt, carryExt = full_adder(first[0], second[0], carry)
    if sumExt != tempSum:
        summ += str(sumExt)
        # print(tempSum, carry)
    return summ[::-1]


# Umrechnen von Dezimalzahlen in Binärzahlen
def dec_to_bin(dec_string, bits, twos_compl):
    decimal = int(dec_string)
    if bits != 0:
        max_num = pow(2, bits) - 1
        if decimal > max_num:
            return "Maximum value is exceeded: " + str(max_num)
    negative = False
    if decimal < 0:
        decimal = abs(decimal)
        negative = True
    # print(decimal)
    # print(negative)
    binary_string = ""
    while decimal > 0:
        binary = decimal % 2
        binary_string += str(binary)
        decimal = decimal // 2
    binary_string = (bits * "0" + binary_string[::-1])[-bits:]
    # print("binary_string", str(binary_string))
    # print("twos_compl", str(twos_compl))
    if twos_compl:
        binary_string = "0" + binary_string
        # print("binary_string", str(binary_string))
        if negative:
            # print("negative", str(negative))
            negativeBinary = ""
            for x in binary_string:
                negativeBinary += str(int(x) ^ 1)
            # print("negativeBinary", negativeBinary)
            negativeBinary = calc(negativeBinary,
                                  dec_to_bin("1", len(negativeBinary) - 1, True))
            # print("negativeBinary", negativeBinary)
            return negativeBinary
    return binary_string


# Umrechnen von Binärzahlen (8 Bit) in Dezimalzahlen
def bin_to_dec(binary, twos_compl):
    x = len(binary) - 1
    decimal = 0
    step = 1
    while x >= 0:
        # print("decimal", decimal)
        # print("binary[x]", binary[x])
        # print("next", int(binary[x]) * step * (1 if not twos_compl or x != 0 else -1))
        decimal += int(binary[x]) * step * (1 if not twos_compl or x != 0 else -1)
        # print("decimal", decimal)
        # print("step", step)
        step = step * 2
        # print("step", step)
        x -= 1
    return str(decimal)


def subnet_ip_amount(wildcardBinaryList):
    binary = ""
    for x in wildcardBinaryList:
        if x == 1:
            binary += str(x)
    return int(bin_to_dec(binary, False)) + 1


# Umrechnung einer binären Liste zu einer binären und dezimalen Adresse
def bin_list_to_address(binary_list):
    decimal_address = ""
    binary_address = ""
    part = ""
    for x in ipRange:
        # subnetmask += str(subnetmaskBinaryList[bit])
        part += str(binary_list[x])
        if (x + 1) % 8 == 0:
            # print(part)
            decimal_address += bin_to_dec(part, False)
            binary_address += part
            # print(subnetmask)
            part = ""
            if x + 1 != ipRange.stop:
                decimal_address += "."
                binary_address += "."
    return decimal_address, binary_address


def calc_address(addressBinaryList, cidr_count, add):
    addressBinList = addressBinaryList.copy()
    host_part = "0" + "".join(str(x) for x in addressBinList[cidr_count:])
    to_add = dec_to_bin(str(add), len(host_part) - 1, True)
    host_part = calc(host_part, to_add)[1:]

    for x in range(cidr_count, len(addressBinList)):
        addressBinList[x] = int(host_part[x - cidr_count])
    return addressBinList


print("SubnetAnalyzer by Mika Schulz")
network = input("Input a IP/CIDR combination:\n")
networkSplit = network.split("/")

if len(networkSplit) == 2:
    ip = networkSplit[0]
    cidrString = networkSplit[1]
    if valid_ip(ip):
        if valid_cidr(cidrString):


            ipBinaryList = []

            subnetmaskBinaryList = []
            wildcardBinaryList = []

            networkaddressBinaryList = []
            broadcastaddressBinaryList = []

            cidr = int(cidrString)

            # Adresse zu binär
            ipSplit = ip.split(".")
            ipSplitRange = range(0, len(ipSplit))
            for addressPart in ipSplitRange:
                ipBinaryList.extend(list(map(int, dec_to_bin(ipSplit[addressPart], 8, False))))

            # CIDR in Bits
            for i in ipRange:
                if i < cidr:
                    subnetmaskBinaryList.append(1)
                    wildcardBinaryList.append(0)
                else:
                    subnetmaskBinaryList.append(0)
                    wildcardBinaryList.append(1)

            for i in ipRange:
                if ipBinaryList[i] & subnetmaskBinaryList[i]:
                    networkaddressBinaryList.append(1)
                else:
                    networkaddressBinaryList.append(0)

                if ipBinaryList[i] | wildcardBinaryList[i]:
                    broadcastaddressBinaryList.append(1)
                else:
                    broadcastaddressBinaryList.append(0)

            ip, ipBinary = bin_list_to_address(ipBinaryList)
            subnetmask, subnetmaskBinary = bin_list_to_address(subnetmaskBinaryList)
            wildcardmask, wildcardmaskBinary = bin_list_to_address(wildcardBinaryList)
            networkaddress, networkaddressBinary = bin_list_to_address(networkaddressBinaryList)
            broadcastaddress, broadcastaddressBinary = bin_list_to_address(
                broadcastaddressBinaryList)
            usableStart, usableStartBinary = bin_list_to_address(
                calc_address(networkaddressBinaryList, cidr, 1))
            usableEnd, usableEndBinary = bin_list_to_address(
                calc_address(broadcastaddressBinaryList, cidr, -1))
            ipAmount = subnet_ip_amount(wildcardBinaryList)

            print("IP:" + 4*"\t" + ip)
            print("CIDR:" + 4*"\t" + str(cidr))
            print("IPs Possible:" + 3*"\t" + str(ipAmount))
            print("Subnetmask:" + 3*"\t" + subnetmask)
            print("Wildcardmask:" + 3*"\t" + wildcardmask)
            print("Networkaddress:" + 3*"\t" + networkaddress)
            print("Broadcastaddress:" + 2*"\t" + broadcastaddress)
            print("Usable Subnet Range Start:" + 1*"\t" + usableStart)
            print("Usable Subnet Range End:" + 1*"\t" + usableEnd)
            print("IP Binary:" + 3*"\t" + ipBinary)
            print("Subnetmask Binary:" + 2*"\t" + subnetmaskBinary)
            print("Wildcardmask Binary:" + 2*"\t" + wildcardmaskBinary)
            print("Networkaddress Binary:" + 2*"\t" + networkaddressBinary)
            print("Broadcastaddress Binary:" + 1*"\t" + broadcastaddressBinary)

        else:
            error = "Invalid CIDR. CIDR must be between 0 and 32. Format: XXX.XXX.XXX.XXX/XX"
    else:
        error = "Invalid Ip. IP parts must be between 0 and 255. Format: XXX.XXX.XXX.XXX/XX"
else:
    error = "Invalid IP/CIDR combination. Format: XXX.XXX.XXX.XXX/XX"

# def calc_subnet(free_ip, cidr=None):


input()
