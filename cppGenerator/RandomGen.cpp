#include "RandomGen.h"
void Generator::SetSeed(std::int64_t seed)
{
    this->gen = std::mt19937_64(seed);
    this->isLive = true;
}
int Generator::TryGen()
{
    if (this->isLive)
    {
        auto number = this->gen.value()();
        auto byte = reinterpret_cast<unsigned char *>(&number)[0];
        return int(byte);
    }
    return -1;
}
