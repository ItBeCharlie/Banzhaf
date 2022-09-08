ex1_1_1 = [6, 4, 3, 2, 1]  # Example input from 1.1.1
nassau = [16, 9, 9, 7, 3, 1, 1]  # Example input from 2
usec = [61, 55, 38, 29]

# Single is in reference to a single required vote value to pass
# in our case, this would be the 50% or 66% threshold.
# In commented code at the bottom is for a bi-party system like
# the one used by the Electoral College


def calc_bpi_single(input):
    # Required number of votes to pass
    required = input[0]

    # Trimming off the first required value
    input = input[1:]

    # print(required, input)

    # Get the indexes that are swing votes and also
    # get the unique indexes used for counting the number
    # of swing votes a single voter influences
    swing_indexes = swing_single(input, required)
    unique_swing_indexes = dict.fromkeys(swing_indexes)

    print(swing_indexes)
    # print(unique_swing_indexes)

    # Initialize all counts to 0
    for key in unique_swing_indexes:
        unique_swing_indexes[key] = 0

    # print(unique_swing_indexes)

    # For each swing vote, increment the number
    # of times that voter has been the swing vote
    for index in swing_indexes:
        unique_swing_indexes[index] += 1

    print(unique_swing_indexes)

    # Create an array with the probabilities each
    # voter is the swing vote
    bpi = [0] * len(input)

    # Generate the bpi
    for i in range(len(bpi)):
        if i in unique_swing_indexes.keys():
            bpi[i] = unique_swing_indexes[i] / len(swing_indexes)

    # print(bpi)

    return bpi


def swing_single(input, required):
    # Generates all binary numbers of length n
    # which represents the possible votes in a
    # 2 party system, where 0 is one party
    # and 1 represents the other party
    bits = [x for x in allBits(len(input))]

    swing_indexes = []

    for bit in bits:
        vote_val = 0
        for i in range(len(input)):
            # For each bit a 0 represents a 'yes' and a 1 represents a 'no'
            if int(bit[i]) == 0:
                # If a member should vote then add their value to the overall vote
                vote_val += input[i]

        # To test if a member is a swing vote, we change their 'yes' to a 'no'
        # We do not test the other way around because of the binary nature,
        # we could inversely change every 'no' to a 'yes' and yield the same result
        for i in range(len(input)):
            swap_val = vote_val
            if int(bit[i]) == 0:
                swap_val -= input[i]

            # This condition checks if changing the single vote actually changes
            # the overall result of the entire vote
            if (swap_val >= required) != (vote_val >= required):
                # Store the index that is a swing vote
                swing_indexes.append(i)
        # print(vote_val)
    # print(swing_indexes)
    # print('\n')

    return swing_indexes


def allBits(n):
    if n:
        yield from (bits+bit for bits in allBits(n-1) for bit in ("0", "1"))
    else:
        yield ""


print(calc_bpi_single(usec))

# Ignore code below, it was all unused in the current iteration of the program


# def calc_bpi_bi(input):
#     # Required number of votes to pass
#     required = input[0]

#     # Trimming off the first required value
#     input = input[1:]

#     print(required, input)

#     # Generates a list of all possible sets based on the input
#     subsets = [x for x in powerset(input)]
#     # print(subsets)

#     # Trims down the list to only the sets where the number of votes can pass
#     # i.e. sum(set) >= required
#     required_sets = []
#     for set in subsets:
#         if sum(set) >= required:
#             required_sets.append(set)

#     # print(required_sets)

#     # for set in required_sets:
#     #     swing_votes(set, required)

#     swing_indexes = swing_single(input, required)
#     unique_swing_indexes = dict.fromkeys(swing_indexes)
#     print(unique_swing_indexes)

#     for key in unique_swing_indexes:
#         unique_swing_indexes[key] = 0

#     print(unique_swing_indexes)

#     for index in swing_indexes:
#         unique_swing_indexes[index] += 1

#     print(unique_swing_indexes)

#     bpi = [0] * len(input)

#     for i in range(len(bpi)):
#         if i in unique_swing_indexes.keys():
#             bpi[i] = unique_swing_indexes[i] / len(swing_indexes)

#     print(bpi)


# def powerset(s):
#     x = len(s)
#     masks = [1 << i for i in range(x)]
#     for i in range(1, 1 << x):
#         yield [ss for mask, ss in zip(masks, s) if i & mask]


# def swing_bi_party(input):
#     # Generates all binary numbers of length n
#     # which represents the possible votes in a
#     # 2 party system, where 0 is one party
#     # and 1 represents the other party
#     votes = [x for x in allBits(len(input))]

#     swing_indexes = []

#     for vote in votes:
#         vote_vals = [0, 0]
#         for i in range(len(input)):
#             vote_vals[int(vote[i])] += input[i]

#         for i in range(len(input)):
#             swap_vals = vote_vals.copy()
#             swap_vals[int(vote[i])] -= input[i]
#             swap_vals[(int(vote[i])+1) % 2] += input[i]

#             if (swap_vals[0] > swap_vals[1]) != (vote_vals[0] > vote_vals[1]):
#                 swing_indexes.append(i)
#         print(vote_vals)
#     print(swing_indexes)
#     print('\n')

#     return swing_indexes
