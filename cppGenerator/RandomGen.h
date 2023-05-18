#pragma once
#include <iostream>
#include <random>
#include <cstdint>
#include <optional>
class Generator{
private:
    std::optional<std::mt19937_64> gen;
    bool isLive = false;
public:
    void SetSeed(std::int64_t seed);
    int TryGen();
};

extern "C" Generator* GetGenerator(){
    return new Generator();
}
extern "C" void StartGenerator(Generator* gen, long long seed){
    gen->SetSeed(seed);
}

extern "C" int TryGen(Generator* gen){
    return gen->TryGen();
}

extern "C" void FreeGen(Generator* gen){
    delete gen;
}