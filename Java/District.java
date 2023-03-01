class District {
    private int number;
    private int population;
    private double populationProportion;
    private int votesPerMember;
    private double normBpi;
    private double bpiDiff;

    public District(int number) {
        this.number = number;
    }

    public int getNumber() {
        return this.number;
    }

    public int getPopulation() {
        return this.population;
    }

    public double getPopulationProportion() {
        return this.populationProportion;
    }

    public int getVotesPerMember() {
        return this.votesPerMember;
    }

    public double getNormBpi() {
        return this.normBpi;
    }

    public double getBpiDiff() {
        return this.bpiDiff;
    }

    public void setPopulation(int population) {
        this.population = population;
    }

    public void setPopulationProportion(double populationProportion) {
        this.populationProportion = populationProportion;
    }

    public void setVotesPerMember(int votesPerMember) {
        this.votesPerMember = votesPerMember;
    }

    public void setNormBpi(double normBpi) {
        this.normBpi = normBpi;
    }

    public void setBpiDiff(double bpiDiff) {
        this.bpiDiff = bpiDiff;
    }

    public District clone() {
        District clone = new District(this.number);
        clone.setPopulation(this.population);
        clone.setBpiDiff(this.bpiDiff);
        clone.setNormBpi(this.normBpi);
        clone.setPopulationProportion(this.populationProportion);
        clone.setVotesPerMember(this.votesPerMember);
        return clone;
    }
}
