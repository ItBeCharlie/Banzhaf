class Main {
    public static void main(String[] args) {
        double[] scores = BPICalculator.calculateBPI(6, new int[] { 4, 3, 2, 1 });

        for (double score : scores)
            System.out.println(score);
    }
}
