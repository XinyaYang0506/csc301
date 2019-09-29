import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class Main {
    // this function traverse the tree and find number of nodes reachable at exactly k distance.
    public static void findkthDistance(int [] kthDistance, LinkedList<Integer> temp,int curNode, LinkedList<Integer>[] isPointedBy, boolean[] cycles, int k) {
        temp.add(curNode);
        if (temp.size() >= k + 1) {
            int ancestor = temp.get(temp.size() - k - 1);
            kthDistance[ancestor]++;
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

    // this function traverse the tree and record number of nodes at each depth level
    public static void findStructure(ArrayList<Integer> chain, int curNode, int depth, LinkedList<Integer>[] isPointedBy, boolean[] cycles) {
        int chainSize = chain.size();
        if (chainSize <= depth) {
            chain.add(0);
        }
        chain.set(depth, chain.get(depth) + 1); //update the value
        if (isPointedBy[curNode] != null) {
            for (Integer node : isPointedBy[curNode]) {
                if (!cycles[node]) {
                    findStructure(chain, node, depth + 1, isPointedBy, cycles);
                }

            }

        }
    }

    // this function calculate the number of nodes  in the tree reachable with in k distance.
    public static void calculateKInChain (int[] ret, int[] kthDistance, int curNode, LinkedList<Integer>[] isPointedBy, boolean[] cycles) {
        ret[curNode] += 1;
        if (isPointedBy[curNode] == null){
            return;
        }
        else {
            for (Integer node : isPointedBy[curNode]) {
                if (!cycles[node]) {
                    calculateKInChain(ret, kthDistance, node, isPointedBy, cycles);
                    ret[curNode] += ret[node];
                    ret[curNode] -= kthDistance[node];
                }
            }


        }
    }


    public static void Solution (int[] stations, int k) {
        int l = stations.length;
        boolean[] checked = new boolean [l];
        LinkedList<Integer>[] nodesPointTo = new LinkedList[l];
        boolean[] inCycle = new boolean[l];

        //find the nodes on the cycle and record each node is pointed to by what.
        for (int i = 0; i < l; i++) {
            int startSt = i;
            boolean [] visited = new boolean [l];
            boolean foundCycle = false;
                while (!checked[startSt]) {
                    int cur = stations[startSt];
                    if (nodesPointTo[cur] == null) {
                        nodesPointTo[cur] = new LinkedList<Integer>();
                    }
                    nodesPointTo[cur].add(startSt);
                    visited[startSt] = true;
                    checked[startSt] = true;
                    startSt = cur;
                }
                if (visited[startSt]) {
                    //now we reach a entry of a cycle
                    int stop = startSt;
                    while (!inCycle[startSt]){
                        inCycle[startSt] =true;
                        startSt = stations[startSt];
                    }
                }
        }

        ArrayList<Integer>[] structuresOfChains = new ArrayList[l];
        int [] kthDistance = new int[l];
        int [] ret = new int[l];
        //now compute each tail
        for (int i= 0; i < l; i++) {
            if (inCycle[i]) {
                structuresOfChains[i] = new ArrayList<Integer>();
                findStructure(structuresOfChains[i], i, 0, nodesPointTo, inCycle);
                LinkedList<Integer> temp = new LinkedList<>();
                findkthDistance(kthDistance, temp, i, nodesPointTo, inCycle, k);
                calculateKInChain(ret, kthDistance, i, nodesPointTo, inCycle);
            }
        }

        //now we consider the  inCycle
        int [] nodesFromCycle = new int[l];
        for (int i= 0; i < l; i++) {
            if (inCycle[i]) {
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

        //combine the result
        for (int i = 0; i < l; i++) {
            ret[i] += nodesFromCycle[i];
            System.out.println(ret[i]);
        }

    }

    public static void main(String[] args) throws FileNotFoundException {
        File file = new File("/Users/xinya/Downloads/icpc2019data/H-hobsonstrains/secret-11.in");
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
