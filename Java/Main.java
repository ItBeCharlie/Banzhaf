class Main {
    public static void main(String[] args) {
        int[] test1 = new int[] { 4, 3, 2, 1 }; // q: 6
        int[] test2 = new int[] { 4195, 3708, 3239, 2715, 1254, 1112, 2020, 403, 1976, 1340, 1285, 4901, 975, 2368,
                5325, 758 };
        double[] scores = BPICalculator.calculateBPI(16, test2);

        for (double score : scores)
            System.out.println(score);
    }
}
