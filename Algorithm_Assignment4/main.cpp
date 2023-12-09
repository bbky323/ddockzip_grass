#include <iostream>
#include <vector>
#include <climits>

using namespace std;

struct Edge {
    int from, to, weight;
};

int bellmanFord(const vector<Edge>& edges, int N, int start, int middle, int end) {
    vector<int> distance1(N, INT_MAX);
    vector<int> distance2(N, INT_MAX);

    distance1[start] = 0;
    distance2[middle] = 0;

    // s에서 a까지의 최단 거리 계산
    for (int i = 0; i < N - 1; ++i) {
        for (const Edge& edge : edges) {
            if (distance1[edge.from] != INT_MAX && distance1[edge.from] + edge.weight < distance1[edge.to]) {
                distance1[edge.to] = distance1[edge.from] + edge.weight;
            }
        }
    }

    // a에서 t까지의 최단 거리 계산
    for (int i = 0; i < N - 1; ++i) {
        for (const Edge& edge : edges) {
            if (distance2[edge.from] != INT_MAX && distance2[edge.from] + edge.weight < distance2[edge.to]) {
                distance2[edge.to] = distance2[edge.from] + edge.weight;
            }
        }
    }

    int result = distance1[middle] + distance2[end];

    return result;
}

int main() {
    int N, M;
    cin >> N >> M;

    int s, a, t;
    cin >> s >> a >> t;

    vector<Edge> edges;

    for (int i = 0; i < M; ++i) {
        int U, V, W;
        cin >> U >> V >> W;
        edges.push_back({U, V, W});
    }

    int result = bellmanFord(edges, N, s, a, t);

    if (result == INT_MAX) {
        cout << "경로가 없습니다." << endl;
    } else {
        cout << result << endl;
    }

    return 0;
}
