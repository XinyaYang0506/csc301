import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class Main {
    public static void findkthDistance(List<Integer> [] kthDistance, LinkedList<Integer> temp,int curNode, LinkedList<Integer>[] isPointedBy, boolean[] cycles, int k) {
        temp.add(curNode);
        if (temp.size() >= k + 1) {
            int ancestor = temp.get(temp.size() - k - 1);
            if (kthDistance[ancestor] == null) {
                kthDistance[ancestor] = new LinkedList<>();
            }
            kthDistance[ancestor].add(curNode);
        }
        if (isPointedBy[curNode] != null) {
            for (Integer node : isPointedBy[curNode]) {
                if (!cycles[node]) {
                    findkthDistance(kthDistance, temp,node, isPointedBy, cycles, k);
                }
            }

        }
        temp.removeLast();
    }

    public static void findStructure(ArrayList<Integer> chain, int curNode, int depth, int[][] numStationsInDistance, LinkedList<Integer>[] isPointedBy, boolean[] cycles, int k) {
        int chainSize = chain.size();
        if (chainSize <= depth) {
            chain.add(0);
        }
        chain.set(depth, chain.get(depth) + 1); //update the value
        if (isPointedBy[curNode] != null) {
            for (Integer node : isPointedBy[curNode]) {
                if (!cycles[node]) {
                    findStructure(chain, node, depth + 1, numStationsInDistance, isPointedBy, cycles, k);
                }

            }

        }


    }

    public static void calculateKInChain (int[] ret, List<Integer>[] kthDistance, int curNode, LinkedList<Integer>[] isPointedBy, boolean[] cycles, int k) {
        ret[curNode] += 1;
        if (isPointedBy[curNode] == null){
            return;
        }
        else {
            for (Integer node : isPointedBy[curNode]) {
                if (!cycles[node]) {
                    calculateKInChain(ret, kthDistance, node, isPointedBy, cycles, k);
                    ret[curNode] += ret[node];
                    ret[curNode] -= kthDistance[node] == null ? 0 : kthDistance[node].size();
                }
            }


        }




    }


    public static void Solution (int[] stations, int k) {
        int l = stations.length;
        boolean[] checked = new boolean [l];
        LinkedList<Integer>[] isPointedBy = new LinkedList[l];
        boolean[] cycles = new boolean[l];

        for (int i = 0; i < l; i++) {
            int startSt = i;
            boolean [] visited = new boolean [l];
            boolean foundCycle = false;
                while (!checked[startSt]) {
                    int cur = stations[startSt];
                    if (isPointedBy[cur] == null) {
                        isPointedBy[cur] = new LinkedList<Integer>();
                    }
                    isPointedBy[cur].add(startSt);
                    visited[startSt] = true;
                    checked[startSt] = true;
                    startSt = cur;
                }
                if (visited[startSt]) {
                    //now we reach a entry of a cycle
                    int stop = startSt;
                    while (!cycles[startSt]){
                        cycles[startSt] =true;
                        startSt = stations[startSt];
                    }
                }
        }
        int [][] numStationsInDistance = new int[l][k + 1];
        ArrayList<Integer>[] structuresOfChains = new ArrayList[l];
        List<Integer> [] kthDistance = new List[l];
        int [] ret = new int[l];
        //now compute each tail
        for (int i= 0; i < l; i++) {
            if (cycles[i]) {
                structuresOfChains[i] = new ArrayList<Integer>();
                findStructure(structuresOfChains[i], i, 0, numStationsInDistance, isPointedBy, cycles, k);
                LinkedList<Integer> temp = new LinkedList<>();
                findkthDistance(kthDistance, temp, i, isPointedBy, cycles, k);
                calculateKInChain(ret, kthDistance, i, isPointedBy, cycles, k);
            }
        }

        int [] nodesFromCycle = new int[l];
        //now we consider the  cycles
        for (int i= 0; i < l; i++) {
            if (cycles[i]) {
                int counter = 1;
                int targetNode = stations[i];
                int usable = ret[i];
                int depthOfTree = structuresOfChains[i].size();
                while (usable > 0 && counter <= k && targetNode != i) {
                    int expired = k - counter + 1 > depthOfTree - 1 ? 0 : structuresOfChains[i].get(k - counter + 1);
                    usable -= expired;
                    nodesFromCycle[targetNode] += usable;
                    targetNode = stations[targetNode];
                    counter++;
                }
            }
        }

        for (int i = 0; i < l; i++) {
            ret[i] += nodesFromCycle[i];
            System.out.println(ret[i]);
        }

    }

    public static void main(String[] args) throws FileNotFoundException {
        File file = new File("/Users/xinya/Downloads/icpc2019data/H-hobsonstrains/secret-45.in");
        Scanner sc = new Scanner(file);
        String [] firstLine = sc.nextLine().split(" ");
        int n = Integer.parseInt(firstLine[0]);
        int k = Integer.parseInt(firstLine[1]);
        int [] stations = new int [n];
        System.out.println("Input: ");
        for (int i = 0; i < n; i++) {
            stations[i] = Integer.parseInt(sc.nextLine()) - 1;
            System.out.println(stations[i] + 1);
        }
        System.out.println("Output: ");
        Solution(stations, k);

    }
}
