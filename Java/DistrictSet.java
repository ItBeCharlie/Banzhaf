class DistrictSet {
    private District[] districts;
    private int votes;
    private double franklinScore;
    private double bpiDiffSum;

    public DistrictSet(District[] districts, int votes) {
        this.districts = districts;
        this.votes = votes;
    }

    /**
     * Calculates this.franklinScore for the district set by adding the top 2
     * absolute values among the districts bpiDiffs
     */
    public void calculateFranklinScore() {
        double firstValue = 0;
        double secondValue = 0;

        for (int i = 1; i < this.districts.length; i++) {
            if (Math.abs(this.districts[i].getBpiDiff()) > firstValue) {
                secondValue = firstValue;
                firstValue = Math.abs(this.districts[i].getBpiDiff());
            } else if (Math.abs(this.districts[i].getBpiDiff()) > secondValue) {
                secondValue = Math.abs(this.districts[i].getBpiDiff());
            }
        }

        this.franklinScore = firstValue + secondValue;
    }

    /**
     * Calculates this.bpiDiffSum for the district set by adding all the
     * absolute values among the districts bpiDiffs
     */
    public void calculateBpiDiffSum() {
        double sum = 0;
        for (District district : this.districts)
            sum += Math.abs(district.getBpiDiff());
        this.bpiDiffSum = sum;
    }

}
