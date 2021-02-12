#include<cstdio>
#include<iomanip>
#include<iostream>
#include<mpi.h>
int main(int argc, char** argv) {

        MPI_Init(&argc, &argv);

        int world_rank;
        MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

        int N;
        long double begin, end, total;

        if (world_rank == 0) {
                std::cin >> N;
                begin = MPI_Wtime();

                long double i_0 = 0;
                long double x_1 = 0;
                long double x_2 = 1.0 / N;

                for (int i = 0; i < N; ++i) {
                        i_0 += (4.0 / (1 + x_1 * x_1) + 4.0 / (1 + x_2 * x_2)) / (2 * N);
                        x_1 += 1.0 / N;
                        x_2 += 1.0 / N;
                }

                end = MPI_Wtime();
                total = end - begin;
                std::cout << "solo: N = " << N << " time = " << std::setprecision(20) << total << std::endl;
                //std::cout << "I_0 = " << std::setprecision(20) << i_0 << std::endl;
        }
        MPI_Finalize();
        return 0;
}

