from conans import ConanFile, AutoToolsBuildEnvironment, tools


class LuajitsolConan(ConanFile):
    name = "luajit-sol"
    version = "0.1"
    license = "MIT"
    url = "https://github.com/veyroter/conan-luajit-sol"
    description = "luajit + sol2 conan recipe"
    settings = "os", "compiler", "build_type", "arch"
    options = {"static": [True, False]}
    default_options = "static=True"
    exports_sources = "src/*"

    sol_version = "2.20.4"
    jit_version = "2.1.0-beta3"

    def source(self):
        sol_url = "https://github.com/ThePhD/sol2/releases/download/v%s/sol.hpp" % self.sol_version
        jit_url = "https://github.com/LuaJIT/LuaJIT/archive/v%s.zip" % self.jit_version
        tools.get(jit_url)
        tools.download(sol_url, "sol.hpp")

    def build(self):
        self.run("ls -la")
        autotools = AutoToolsBuildEnvironment(self)
        env_build_vars = autotools.vars
        make_dir_arg = "-CLuaJIT-%s" % self.jit_version
        autotools.make(vars=env_build_vars, args=[make_dir_arg])
        autotools.install(vars=env_build_vars, args=[
                          make_dir_arg, "PREFIX=%s" % self.install_folder])

    def package(self):
        self.copy("*.h", src="include", dst="include", keep_path=False)
        self.copy("*.hpp", dst="include", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["luajit"]  # TODO
        else:
            self.cpp_info.libs = [
                "libluajit.a"] if self.options.static else ["libluajit.so"]

        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["dl", "m"])
