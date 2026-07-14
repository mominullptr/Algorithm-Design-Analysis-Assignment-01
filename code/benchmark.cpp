#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <fstream>
#include <string>
#include <cmath>
#include <cassert>
#include <numeric>

using namespace std;
using namespace std::chrono;

// Global Mersenne Twister PRNG engine (replaces C-style rand() for better
// statistical properties and no modulo bias)
static mt19937 rng_engine(1337);

// Pivot choice mapping:
// 1 = First Element
// 2 = Last Element
// 3 = Middle Element
// 4 = Random Element

// Partition function using pivot-preswap scheme:
// 1. Select pivot based on strategy (first/last/middle/random)
// 2. Swap chosen pivot to arr[low] position
// 3. Scan from both ends to partition elements around pivot
// 4. Place pivot in its final sorted position
int partition(vector<int> &arr, int low, int high, int pivotChoice)
{
    // Step 1: Choose pivot element and swap it to the front (arr[low])
    // This normalizes all strategies so the partitioning logic below is uniform.
    if (pivotChoice == 2)
    {
        // Last Element: swap last element to front
        swap(arr[low], arr[high]);
    }
    else if (pivotChoice == 3)
    {
        // Middle Element: swap element at floor(n/2) to front
        int mid = low + (high - low) / 2;
        swap(arr[low], arr[mid]);
    }
    else if (pivotChoice == 4)
    {
        // Random Element: swap a uniformly random element to front
        uniform_int_distribution<int> dist(low, high);
        int randomIndex = dist(rng_engine);
        swap(arr[low], arr[randomIndex]);
    }
    // pivotChoice == 1: First Element — already at arr[low], no swap needed

    // Step 2: Partition around the pivot (now at arr[low])
    // Elements <= pivot go to the left; elements > pivot go to the right.
    int pivot = arr[low];
    int i = low + 1;  // Left scanner: moves right, looking for elements > pivot
    int j = high;     // Right scanner: moves left, looking for elements <= pivot

    while (true)
    {
        // Advance left scanner past elements that are <= pivot
        while (i <= high && arr[i] <= pivot)
            i++;

        // Advance right scanner past elements that are > pivot
        while (arr[j] > pivot)
            j--;

        // If scanners haven't crossed, swap the misplaced pair
        if (i < j)
            swap(arr[i], arr[j]);
        else
            break;
    }

    // Step 3: Place pivot in its final sorted position
    // j now points to the last element <= pivot; swap pivot there
    swap(arr[low], arr[j]);
    return j;
}

void quickSort(vector<int> &arr, int low, int high, int pivotChoice, int currentDepth, int &maxDepth)
{
    if (currentDepth > maxDepth)
    {
        maxDepth = currentDepth;
    }
    
    if (low < high)
    {
        int pivotIndex = partition(arr, low, high, pivotChoice);

        quickSort(arr, low, pivotIndex - 1, pivotChoice, currentDepth + 1, maxDepth);
        quickSort(arr, pivotIndex + 1, high, pivotChoice, currentDepth + 1, maxDepth);
    }
}

vector<int> generateRandomArray(int size)
{
    uniform_int_distribution<int> dist(0, 99999);
    vector<int> arr(size);
    for (int i = 0; i < size; ++i)
    {
        arr[i] = dist(rng_engine);
    }
    return arr;
}

vector<int> generateAscendingArray(int size)
{
    vector<int> arr(size);
    for (int i = 0; i < size; ++i)
    {
        arr[i] = i;
    }
    return arr;
}

vector<int> generateDescendingArray(int size)
{
    vector<int> arr(size);
    for (int i = 0; i < size; ++i)
    {
        arr[i] = size - i;
    }
    return arr;
}

// Calculate mean and sample standard deviation
void calculateStats(const vector<double> &data, double &mean, double &stddev)
{
    double sum = std::accumulate(data.begin(), data.end(), 0.0);
    mean = sum / data.size();

    double sq_sum = 0.0;
    for (double val : data)
    {
        sq_sum += (val - mean) * (val - mean);
    }
    // Using sample standard deviation (Bessel's correction: N-1) for statistical rigor
    stddev = (data.size() > 1) ? sqrt(sq_sum / (data.size() - 1)) : 0.0;
}

void runExperiment(string arrayType, string fileName)
{
    ofstream out(fileName);
    out << "Size,First_mean,First_std,Last_mean,Last_std,Middle_mean,Middle_std,Random_mean,Random_std\n";

    int maxLimit = 5000;
    int step = 10;
    int repetitions = 30;

    cout << "Running experiment for " << arrayType << " arrays..." << endl;

    for (int size = 10; size <= maxLimit; size += step)
    {
        vector<double> timesFirst(repetitions);
        vector<double> timesLast(repetitions);
        vector<double> timesMiddle(repetitions);
        vector<double> timesRandom(repetitions);

        for (int rep = 0; rep < repetitions; ++rep)
        {
            vector<int> baseArr;
            if (arrayType == "random")
                baseArr = generateRandomArray(size);
            else if (arrayType == "ascending")
                baseArr = generateAscendingArray(size);
            else
                baseArr = generateDescendingArray(size);

            int dummyDepth = 0;

            vector<int> arr1 = baseArr;
            auto start1 = high_resolution_clock::now();
            quickSort(arr1, 0, arr1.size() - 1, 1, 1, dummyDepth);
            auto stop1 = high_resolution_clock::now();
            timesFirst[rep] = duration_cast<nanoseconds>(stop1 - start1).count() / 1000.0; // Store in microseconds

            dummyDepth = 0;
            vector<int> arr2 = baseArr;
            auto start2 = high_resolution_clock::now();
            quickSort(arr2, 0, arr2.size() - 1, 2, 1, dummyDepth);
            auto stop2 = high_resolution_clock::now();
            timesLast[rep] = duration_cast<nanoseconds>(stop2 - start2).count() / 1000.0;

            dummyDepth = 0;
            vector<int> arr3 = baseArr;
            auto start3 = high_resolution_clock::now();
            quickSort(arr3, 0, arr3.size() - 1, 3, 1, dummyDepth);
            auto stop3 = high_resolution_clock::now();
            timesMiddle[rep] = duration_cast<nanoseconds>(stop3 - start3).count() / 1000.0;

            dummyDepth = 0;
            vector<int> arr4 = baseArr;
            auto start4 = high_resolution_clock::now();
            quickSort(arr4, 0, arr4.size() - 1, 4, 1, dummyDepth);
            auto stop4 = high_resolution_clock::now();
            timesRandom[rep] = duration_cast<nanoseconds>(stop4 - start4).count() / 1000.0;
        }

        double meanFirst, stdFirst;
        double meanLast, stdLast;
        double meanMiddle, stdMiddle;
        double meanRandom, stdRandom;

        calculateStats(timesFirst, meanFirst, stdFirst);
        calculateStats(timesLast, meanLast, stdLast);
        calculateStats(timesMiddle, meanMiddle, stdMiddle);
        calculateStats(timesRandom, meanRandom, stdRandom);

        out << size << ","
            << meanFirst << "," << stdFirst << ","
            << meanLast << "," << stdLast << ","
            << meanMiddle << "," << stdMiddle << ","
            << meanRandom << "," << stdRandom << "\n";
    }

    out.close();
    cout << "Completed: " << arrayType << " arrays. Results written to " << fileName << endl;
}

// Correctness self-test: checks that all strategies sort array correctly
void runSelfTest()
{
    cout << "Running correctness self-test..." << endl;
    vector<int> testSizes = {10, 50, 200, 1000};
    
    for (int size : testSizes)
    {
        for (int pivotChoice = 1; pivotChoice <= 4; ++pivotChoice)
        {
            vector<int> arr = generateRandomArray(size);
            int maxDepth = 0;
            quickSort(arr, 0, arr.size() - 1, pivotChoice, 1, maxDepth);
            
            // Verify array is sorted ascending
            for (size_t i = 1; i < arr.size(); ++i)
            {
                if (arr[i] < arr[i - 1])
                {
                    cerr << "Self-test FAILED for size " << size << ", strategy " << pivotChoice << "!" << endl;
                    exit(1);
                }
            }
        }
    }
    cout << "Self-test PASSED. All pivot selection strategies are verified correct." << endl;
}

void instrumentRecursionDepth()
{
    cout << "Instrumenting maximum recursion depth on worst-case inputs (N = 5000)..." << endl;
    int size = 5000;
    
    // 1. First pivot on Ascending Array
    {
        vector<int> arr = generateAscendingArray(size);
        int maxDepth = 0;
        quickSort(arr, 0, arr.size() - 1, 1, 1, maxDepth);
        cout << "  First Element Pivot (Ascending Input): Max Depth = " << maxDepth << " (expected 5000)" << endl;
    }
    
    // 2. Last pivot on Ascending Array
    {
        vector<int> arr = generateAscendingArray(size);
        int maxDepth = 0;
        quickSort(arr, 0, arr.size() - 1, 2, 1, maxDepth);
        cout << "  Last Element Pivot (Ascending Input): Max Depth = " << maxDepth << " (expected 5000)" << endl;
    }
    
    // 3. Middle pivot on Ascending Array
    {
        vector<int> arr = generateAscendingArray(size);
        int maxDepth = 0;
        quickSort(arr, 0, arr.size() - 1, 3, 1, maxDepth);
        cout << "  Middle Element Pivot (Ascending Input): Max Depth = " << maxDepth << endl;
    }
    
    // 4. Random pivot on Ascending Array
    {
        vector<int> arr = generateAscendingArray(size);
        int maxDepth = 0;
        quickSort(arr, 0, arr.size() - 1, 4, 1, maxDepth);
        cout << "  Random Element Pivot (Ascending Input): Max Depth = " << maxDepth << endl;
    }
}

int main()
{
    // rng_engine is already seeded with 1337 at construction (global scope)

    runSelfTest();
    instrumentRecursionDepth();

    runExperiment("random", "data/random_results.csv");
    runExperiment("ascending", "data/ascending_results.csv");
    runExperiment("descending", "data/descending_results.csv");

    cout << "All benchmarks completed successfully." << endl;
    return 0;
}
