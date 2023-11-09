from District import District
from DistrictSet import DistrictSet
from optimizer import optimize
import datetime


def run_program(initial_district_set, votes, max_votes=501):
    district_set = initial_district_set.clone()

    # Save a copy of the original data
    orig_districts = district_set.clone()

    # Reset votes for incrementer
    votes = 1

    # Keep track of the best franklin score and set
    best_franklin_score = 99999
    best_set = district_set.clone()
    best_66 = district_set.clone()
    best_66.generate_data(quota=(best_66.votes*2)//3)

    # Store all district sets based off 50% and 2/3 voting systems
    district_sets_50 = []
    district_sets_66 = []

    for new_votes in range(votes+100, max_votes, 100):
        # Change the district set to have the current interation of votes
        district_set = best_set.clone()
        district_set.override_votes(new_votes)

        # Run the district through the optimizer
        district_set = optimize(district_set, iterations=50)

        # Calculate the data for the 2/3 quota district set
        district_set_66 = district_set.clone()
        district_set_66.generate_data(quota=(new_votes*2)//3)

        # Get the franklin score
        district_set.franklin_score()
        current_franklin_score = district_set.franklin

        # Check if this district_set is the most optimal franklin so far
        if current_franklin_score < best_franklin_score:
            best_franklin_score = current_franklin_score
            best_set = district_set.clone()
            best_66 = district_set_66.clone()

        # Store both district sets for the two quotas
        district_sets_50.append(district_set.clone())
        district_sets_66.append(district_set_66.clone())
    return best_set

def main():
    global time
    time = datetime.datetime.now()
    time = time.strftime('%m-%d-%y-%H-%M-%S')

    print(time)
    district_set = test_read('case1.txt')
    best_district_set = run_program(district_set, district_set.votes, 1501)
    print(best_district_set)


def test_read(file):
    global time  # TEMP
    with open(file) as f:
        lines = f.readlines()
    votes = int(lines[0])
    districts = []
    for i in range(1, len(lines)):
        districts.append(District(str(i-1), i-1))
        districts[i-1].population = int(lines[i])

    return DistrictSet(districts, votes, time, initial=True)


main()
