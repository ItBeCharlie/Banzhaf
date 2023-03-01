class BPICalculator {

    /**
     * 
     * @param q The quota to be met. The rest must be the voting powers for each
     *          player
     * @param S The voting powers for each player
     * 
     * @return The normalized BPI score for each player
     */
    public static double[] calculateBPI(int q, int[] S) {
        int[] scores = new int[S.length];

        for (int index = 0; index < S.length; index++) {
            int[][] f = buildFTable(q, copyArray(S), index);
            int score = 0;
            for (int y = q - S[index]; y < q; y++)
                score += f[f.length - 2][y];
            scores[index] = score;
            System.out.println(score);
        }
        return normalizeScores(scores);
    }

    private static int[] copyArray(int[] a) {
        int[] copy = new int[a.length];
        for (int i = 0; i < a.length; i++)
            copy[i] = a[i];
        return copy;
    }

    private static double[] normalizeScores(int[] scores) {
        double[] normScores = new double[scores.length];

        // Get the sum of all the scores
        double totalScore = 0;
        for (int i = 0; i < scores.length; i++)
            totalScore += scores[i];

        for (int i = 0; i < scores.length; i++)
            normScores[i] = scores[i] / totalScore;

        return normScores;
    }

    /**
     * 
     * @param q Quota needed in the system for a vote to pass
     * @param S Voting power of each player
     * @param p Current player table is generated for
     *          Players must be 0-indexed
     * @return F table used for find Banzhaf Index
     */
    private static int[][] buildFTable(int q, int[] S, int p) {
        // Initializing empty table
        int[][] table = new int[S.length + 1][q];

        // Priming table for alg by setting top left cell to 1
        table[0][0] = 1;

        // Swap the voting powers of last player and the player p we are generating
        // table for
        int temp = S[p];
        S[p] = S[S.length - 1];
        S[S.length - 1] = temp;

        // Iterate over the previous row of the table, and set the current index as
        // follows:
        // 1. Add table[row-1][col]
        // 2. Add table[row-1][col-S[row]]
        for (int row = 1; row < S.length + 1; row++) {
            for (int col = 0; col < q; col++) {
                // Step 1
                table[row][col] = table[row - 1][col];
                // Step 2
                if (S[row - 1] <= col)
                    table[row][col] += table[row - 1][col - S[row - 1]];
            }
        }

        return table;
    }
}