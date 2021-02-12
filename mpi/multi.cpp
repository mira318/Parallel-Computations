#include<iomanip>
#include<iostream>
#include<mpi.h>
int main(int argc, char** argv) {

        MPI_Init(&argc, &argv);

        int world_size;
        MPI_Comm_size(MPI_COMM_WORLD, &world_size);

        int world_rank;
        MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

        int N;
        long double procc_start;
        long double procc_end;
        long double part_i = 0;
        long double y_1;
        long double y_2;

        MPI_Status stat;
        long double begin, end, total;

        if (world_rank == 0) {
                std::cin >> N;
                begin = MPI_Wtime();
                int rest = N % world_size;

                procc_start = 0;
                procc_end = 1.0 / world_size;

                if (rest > 0) {
                        procc_end += 1.0 / N;
                        rest--;
                }

                for (int p = 1; p < world_size; ++p) {

                        procc_start = procc_end;
                        procc_end = procc_start + 1.0 / world_size;

                        if (rest > 0) {
                                procc_end += 1.0 / N;
                                rest--;
                        }

                        MPI_Send(&procc_start, 1, MPI_LONG_DOUBLE, p, 0, MPI_COMM_WORLD);
                        MPI_Send(&procc_end, 1, MPI_LONG_DOUBLE, p, 0, MPI_COMM_WORLD);
                        MPI_Send(&N, 1, MPI_INT, p, 0, MPI_COMM_WORLD);
                }
                procc_start = 0;
                procc_end = 1.0 / world_size;
                if (N % world_size > 0) {
                        procc_end += 1.0 / N;

                }

        } else {

                MPI_Recv(&procc_start, 1, MPI_LONG_DOUBLE, 0, 0, MPI_COMM_WORLD, &stat);
                MPI_Recv(&procc_end, 1, MPI_LONG_DOUBLE, 0, 0, MPI_COMM_WORLD, &stat);
                MPI_Recv(&N, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &stat);
        }

        y_1 = procc_start;
        y_2 = procc_start + 1.0 / N;

        while(y_2 < procc_end) {

                part_i +=  (4.0 / (1 + y_1 * y_1) + 4.0 / (1 + y_2 * y_2)) / (2 * N);
                y_1 += 1.0 / N;
                y_2 += 1.0 / N;
        }
        if(world_rank == 0) {

                long double ans_in_parts = part_i;
                for(int p = 1; p < world_size; ++p) {

                        MPI_Recv(&part_i, 1, MPI_LONG_DOUBLE, p, 0, MPI_COMM_WORLD, &stat);
                        ans_in_parts += part_i;

                }

                end = MPI_Wtime();
                total = end - begin;
                std::cout << "multi: N = " << N << " p = " << world_size <<" time = " << total << std::endl;
                //std::cout << "I = " << std::setprecision(20) << ans_in_parts << std::endl;

        } else {

                MPI_Send(&part_i, 1, MPI_LONG_DOUBLE, 0, 0, MPI_COMM_WORLD);

        }
        MPI_Finalize();
        return 0;
}

