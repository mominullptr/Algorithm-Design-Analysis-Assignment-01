#include <iostream>
#include <vector>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <string>

using namespace std;
using namespace std::chrono;

// 1 = First Element
// 2 = Last Element
// 3 = Middle Element
// 4 = Random Element

int partition(vector<int> &arr, int low, int high, int pivotChoice)
{
    // Choose Pivot
    if (pivotChoice == 2)
    {
        swap(arr[low], arr[high]);
    }
    else if (pivotChoice == 3)
    {
        int mid = low + (high - low) / 2;
        swap(arr[low], arr[mid]);
    }
    else if (pivotChoice == 4)
    {
        int randomIndex = low + rand() % (high - low + 1);
        swap(arr[low], arr[randomIndex]);
    }

    // Hoare Partition
    int pivot = arr[low];
    int i = low + 1;
    int j = high;

    while (true)
    {
        while (i <= high && arr[i] <= pivot)
            i++;

        while (arr[j] > pivot)
            j--;

        if (i < j)
            swap(arr[i], arr[j]);
        else
            break;
    }

    swap(arr[low], arr[j]);
    return j;
}

void quickSort(vector<int> &arr, int low, int high, int pivotChoice)
{
    if (low < high)
    {
        int pivotIndex = partition(arr, low, high, pivotChoice);

        quickSort(arr, low, pivotIndex - 1, pivotChoice);
        quickSort(arr, pivotIndex + 1, high, pivotChoice);
    }
}

vector<int> generateRandomArray(int size)
{
    vector<int> arr(size);
    for (int i = 0; i < size; ++i)
    {
        arr[i] = rand() % 100000;
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

void runExperiment(string arrayType, string fileName)
{
    ofstream out(fileName);
    out << "Size,First,Last,Middle,Random\n";

    int maxLimit = 5000;
    int step = 10;
    int repetitions = 30;

    cout << "Running experiment for " << arrayType << " arrays..." << endl;

    for (int size = 10; size <= maxLimit; size += step)
    {
        double timeFirst = 0;
        double timeLast = 0;
        double timeMiddle = 0;
        double timeRandom = 0;

        for (int rep = 0; rep < repetitions; ++rep)
        {
            vector<int> baseArr;
            if (arrayType == "random")
                baseArr = generateRandomArray(size);
            else if (arrayType == "ascending")
                baseArr = generateAscendingArray(size);
            else
                baseArr = generateDescendingArray(size);

            vector<int> arr1 = baseArr;
            auto start1 = high_resolution_clock::now();
            quickSort(arr1, 0, arr1.size() - 1, 1);
            auto stop1 = high_resolution_clock::now();
            timeFirst += duration_cast<microseconds>(stop1 - start1).count();

            vector<int> arr2 = baseArr;
            auto start2 = high_resolution_clock::now();
            quickSort(arr2, 0, arr2.size() - 1, 2);
            auto stop2 = high_resolution_clock::now();
            timeLast += duration_cast<microseconds>(stop2 - start2).count();

            vector<int> arr3 = baseArr;
            auto start3 = high_resolution_clock::now();
            quickSort(arr3, 0, arr3.size() - 1, 3);
            auto stop3 = high_resolution_clock::now();
            timeMiddle += duration_cast<microseconds>(stop3 - start3).count();

            vector<int> arr4 = baseArr;
            auto start4 = high_resolution_clock::now();
            quickSort(arr4, 0, arr4.size() - 1, 4);
            auto stop4 = high_resolution_clock::now();
            timeRandom += duration_cast<microseconds>(stop4 - start4).count();
        }

        out << size << ","
            << (timeFirst / repetitions) << ","
            << (timeLast / repetitions) << ","
            << (timeMiddle / repetitions) << ","
            << (timeRandom / repetitions) << "\n";
    }

    out.close();
    cout << "Completed: " << arrayType << " arrays. Results written to " << fileName << endl;
}

int main()
{
    srand(1337);

    runExperiment("random", "random_results.csv");
    runExperiment("ascending", "ascending_results.csv");
    runExperiment("descending", "descending_results.csv");

    cout << "All benchmarks completed successfully." << endl;
    return 0;
}
