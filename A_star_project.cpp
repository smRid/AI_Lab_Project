#include <bits/stdc++.h>

using namespace std;

#define INF 1000000
#define FREE 0
#define BLOCK 1
#define PATH -1

const int N = 101;
int row, column;

pair<int, int> par[N][N];
int Maze[N][N];
double Manhattan_Distance[N][N];
double Diagonal_Distance[N][N];
double Euclidean_Distance[N][N];

int fx[] = {0, -1, 0, +1, -1, -1, +1, +1}; 
int fy[] = {+1, 0, -1, 0, +1, -1, -1, +1};

bool isValid(int currentX, int currentY) {
	return currentX >= 0 and currentX < row and currentY >= 0 and currentY < column;
}

bool isUnBlocked(int row, int col) {
    if (Maze[row][col] == FREE) {
        return true;
    }
    else {
        return false;
    }
}

void Manhattan_Distances (pair <int, int> goal) {
	for(int currentX = 0; currentX < row; currentX++) {
		for(int currentY = 0; currentY < column; currentY++) {
			Manhattan_Distance[currentX][currentY] = abs(goal.first - currentX) + abs(goal.second - currentY);
		}	
	}
}

void Diagonal_Distances (pair <int, int> goal) {
	for(int currentX = 0; currentX < row; currentX++) {
		for(int currentY = 0; currentY < column; currentY++) {
			Diagonal_Distance[currentX][currentY] = max(abs(goal.first - currentX), abs(goal.second - currentY));
		}	
	}
}

void Euclidean_Distances (pair <int, int> goal) {
	for(int currentX = 0; currentX < row; currentX++) {
		for(int currentY = 0; currentY < column; currentY++) {
			Euclidean_Distance[currentX][currentY] = sqrt(((goal.first - currentX) * (goal.first - currentX)) + ((goal.second - currentY) * (goal.second - currentY)));
		}	
	}
}

void AStarSearch(pair <int, int> source, pair <int, int> goal, int d) {
	if (isValid(source.first, source.second) == false) {
        cout << "Source is invalid\n";
        return;
    }
 
    if (isValid(goal.first, goal.second) == false) {
        cout << "Goal is invalid\n";
        return;
    }
 
    if (isUnBlocked(source.first, source.second) == false || isUnBlocked(goal.first, goal.second) == false) {
        cout << "Source or the Goal is blocked\n";
        return;
    }
 
    if (source.first == goal.first && source.second == goal.second) {
        cout << "We are already at the destination\n";
        return;
    }

    double Distance[N][N];
    if (d == 1) {
    	for (int x = 0; x < row; x++) {
    		for (int y = 0; y < column; y++) {
    			Distance[x][y] = Manhattan_Distance[x][y];
    		}
    	}
    }
    else if (d == 2) {
    	for (int x = 0; x < row; x++) {
    		for (int y = 0; y < column; y++) {
    			Distance[x][y] = Diagonal_Distance[x][y];
    		}
    	}
    }
    else {
    	for (int x = 0; x < row; x++) {
    		for (int y = 0; y < column; y++) {
    			Distance[x][y] = Euclidean_Distance[x][y];
    		}
    	}
    }

	double cost[N][N], dist[N][N];
	for (int i = 0; i < row; i++) {
		for (int j = 0; j < column; j++) {
			cost[i][j] = 1.0 * INF;
			dist[i][j] = 1.0 * INF;
		}
	}

	priority_queue <pair <int, int>, vector <pair <int, int>>, greater <pair <int, int>>> pq;
	pq.push(source);
	cost[source.first][source.second] = 0;
	while (!pq.empty()) {
		auto current = pq.top();
		int current_x = current.first;
		int current_y = current.second;
		pq.pop();
		for (int k = 0; k < 4; k++) {
			int nxt_x = current_x + fx[k];
			int nxt_y = current_y + fy[k];
			if (isValid(nxt_x, nxt_y) and Maze[nxt_x][nxt_y] != BLOCK and cost[current_x][current_y] + Distance[current_x][current_y] + 1  < cost[nxt_x][nxt_y]) {
				dist[nxt_x][nxt_y] = dist[current_x][current_y] + 1;
				cost[nxt_x][nxt_y] = cost[current_x][current_y] + Distance[current_x][current_y] + 1;
				par[nxt_x][nxt_y] = make_pair(current_x, current_y);
				pq.push(make_pair(nxt_x, nxt_y));
			}
		}

		for (int k = 4; k < 8; k++) {
			int nxt_x = current_x + fx[k];
			int nxt_y = current_y + fy[k];
			if (isValid(nxt_x, nxt_y) and Maze[nxt_x][nxt_y] != BLOCK and cost[current_x][current_y] + Distance[current_x][current_y] + 1.414  < cost[nxt_x][nxt_y]) {
				dist[nxt_x][nxt_y] = dist[current_x][current_y] + 1;
				cost[nxt_x][nxt_y] = cost[current_x][current_y] + Distance[current_x][current_y] + 1.414;
				par[nxt_x][nxt_y] = make_pair(current_x, current_y);
				pq.push(make_pair(nxt_x, nxt_y));
			}
		}
	}

	if (dist[goal.first][goal.second] == INT_MAX) {
		cout << "Unable to reach at Goal" << '\n';
		return;
	}

	vector <pair <int, int>> path;
	auto cur = goal;
    while (cur != source) {
      path.push_back(cur);
      cur = par[cur.first][cur.second];
    }
    path.push_back(source);
    cout << "Path: [";
  	reverse(path.begin(), path.end());
  	for(int i = 0; i < path.size(); i++) {
  		if(i < path.size() - 1) cout << "(" << path[i].first << ", " << path[i].second << "), ";
  		else cout << "(" << path[i].first << ", " << path[i].second << ")]\n"; 
  	}

  	double pathcost = 0;
  	for (int i = 1; i < path.size(); i++) {
  		if (((path[i].first - path[i - 1].first) * (path[i].first - path[i - 1].first) + (path[i].second - path[i - 1].second) * (path[i].second - path[i - 1].second)) == 1) {
  			pathcost += 1;
  		}
  		else {
  			pathcost += 1.414;
  		}
  	}

	cout << "Path Cost: " << pathcost << '\n';
}

int32_t main() {
   
    auto start = clock();
    printf("Enter the number of row: ");
    cin >> row;
    printf("Enter the number of column: ");
    cin >> column;

    for (int x = 0; x < row; x++) {
    	for (int y = 0; y < column; y++) {
    		Maze[x][y] = FREE;
    	}
    }

    int obstacles;
    printf("Enter the number of obstacle in the entire grid:");
    cin >> obstacles;
    printf("Now enter the co-ordinates of each obstacles\n");
    for (int i = 0; i < obstacles; i++) {
    	int x, y;
    	cin >> x >> y;
    	Maze[x][y] = BLOCK;
    }

	printf("Enter the source's co-ordinates: ");
    pair <int, int> source;
    cin >> source.first >> source.second;

	printf("Enter the goal's co-ordinates: ");
    pair <int, int> goal;
    cin >> goal.first >> goal.second;

    Manhattan_Distances(goal);
    Diagonal_Distances(goal);
    Euclidean_Distances(goal);

    AStarSearch(source, goal, 1);

    AStarSearch(source, goal, 2);

    AStarSearch(source, goal, 3);

    cout << "Time Taken: " << (1.0 * (clock()-start) / CLOCKS_PER_SEC) << " ms\n" ;
    
    return 0;
}