#include <cstdio>
#include <functional>
#include <iostream>
#include <random>

#define BLOCKSIZE 256


void FillMatrix(float* matrix, int height, int width) {
    std::mt19937 gen(time(0));
    std::uniform_real_distribution<float> distribution(-1.0f, 1.0f);
    auto generate = std::bind(distribution, gen);
    for (int i = 0; i < height * width; ++i) {
        matrix[i] = generate();
    }
}

void PrintMatrix(float *matrix, int height, int width) {

    for (int i = 0; i < height; ++i) {
        for (int j = 0; j < width; ++j) {
            std::cout << matrix[i * width + j] << " ";
        }
	std::cout << std::endl;
    }
}


__global__
void kernel_mul(float *A, float *B, float *C, int mid_size) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    int j = blockIdx.y * blockDim.y + threadIdx.y;
    int height = blockDim.x * gridDim.x;
    int width = blockDim.y * gridDim.y;

    C[i * width + j] = 0.0f;
    for (int k = 0; k < mid_size; ++k) {
        C[i * width + j] += A[i * mid_size + k] * B[k * width + j];
    }
}

__global__
void kernel_my_mul(float *A, float *B, float *C, int mid_size) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    int j = blockIdx.y * blockDim.y + threadIdx.y;
    int height = blockDim.x * gridDim.x;
    int width = blockDim.y * gridDim.y;

    __shared__ float block_a[BLOCKSIZE];
    __shared__ float block_b[BLOCKSIZE];

    block_a[threadIdx.y] = A[i * width + threadIdx.y];
    block_b[threadIdx.x] = B[threadIdx.x * height + j];

    __syncthreads();

    C[i * width + j] = 0.0f;
    for (int k = 0; k < mid_size; ++k) {
	C[i * width + j] += block_a[k] * block_b[k];
    }
}

void try_both_multiplications(float *h_A, float *h_B, float *h_C) {
    float* d_A;
    float* d_B;
    float* d_C;

    cudaMalloc(&d_A, sizeof(float) * 128 * 384);
    cudaMalloc(&d_B, sizeof(float) * 384 * 256);
    cudaMalloc(&d_C, sizeof(float) * 128 * 256);

    cudaMemcpy(d_A, h_A, sizeof(float) * 128 * 384, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, sizeof(float) * 384 * 256, cudaMemcpyHostToDevice);

    // kernel call
    dim3 num_blocks(8, 16);
    dim3 block_size(16, 16);

    cudaEvent_t start;
    cudaEvent_t stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    cudaEventRecord(start);
    kernel_mul<<<num_blocks, block_size>>>(d_A, d_B, d_C, 384);

    cudaEventRecord(stop);
    cudaMemcpy(h_C, d_C, sizeof(float) * 128 * 256, cudaMemcpyDeviceToHost);
    cudaEventSynchronize(stop);

    float milliseconds = 0;

    cudaEventElapsedTime(&milliseconds, start, stop);
    std::cout << "banal elapsed in " << milliseconds << std::endl;

    PrintMatrix(h_C, 128, 256);

    cudaEvent_t start2;
    cudaEvent_t stop2;
    cudaEventCreate(&start2);
    cudaEventCreate(&stop2);

    cudaEventRecord(start2);
    kernel_my_mul<<<num_blocks, block_size>>>(d_A, d_B, d_C, 384);

    cudaEventRecord(stop2);
    cudaMemcpy(h_C, d_C, sizeof(float) * 128 * 256, cudaMemcpyDeviceToHost);
    cudaEventSynchronize(stop2);

    float milliseconds2 = 0;

    cudaEventElapsedTime(&milliseconds2, start2, stop2);
    std::cout << "shared memory elapsed in " << milliseconds2 << std::endl;

    PrintMatrix(h_C, 128, 256);

    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
}

int main() {

    float *h_A;
    float *h_B;
    float *h_C;

    // h_A 128 * 384
    // h_B 384 * 256
    // h_C 128 * 256

    h_A = new float[128 * 384];
    h_B = new float[384 * 256];
    h_C = new float[128 * 256];

    FillMatrix(h_A, 128, 384);
    FillMatrix(h_B, 384, 256);
    try_both_multiplications(h_A, h_B, h_C);

    delete[] h_A;
    delete[] h_B;
    delete[] h_C;
    return 0;
}
