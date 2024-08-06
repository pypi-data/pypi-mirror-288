#include "AlignTools.h"

#include <stdexcept>
#include <string>


void AlignTools::handleFailedAssertion(
    const char* expression,
    const char* function,
    const char* file,
    int line)
{
    throw std::runtime_error(
        std::string("Assertion failed: ") + expression +
        " at " + function +
        " in " +  file +
        " line " + std::to_string(line));
}


