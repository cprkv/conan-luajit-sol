#define SOL_CHECK_ARGUMENTS 1
#include <sol.hpp>
#include <iostream>

int main(int, char **)
{
  sol::state lua;
  lua.open_libraries(sol::lib::base, sol::lib::package);
  int value = lua.script("a = function () return 3; end; return a();");

  if (value != 3)
    abort();

  std::cout << "test ok" << std::endl;

  return 0;
}