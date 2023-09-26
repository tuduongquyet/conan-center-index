from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, rmdir, copy
from conan.tools.scm import Version
import os

required_conan_version = ">=1.50.0"


class woff2Conan(ConanFile):
    name = "woff2"
    version = "1.0.2"
    license = "The Web Open Font Format (WOFF) is a font format for use in web pages."
    author = "Tu Duong Quyet <tuduongquyet@gmail.com>"
    url = "https://github.com/tuduongquyet/conan-woff2"
    description = "woff2 is a library to encode and decode WOFF2 font files."
    topics = ("conan", "font", "woff2")

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.cppstd")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires("brotli/1.1.0")

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
            destination=self.source_folder, strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, pattern="LICENSE.md", dst=os.path.join(
            self.package_folder, "licenses"), src=self.source_folder)
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = ["woff2common", "woff2enc", "woff2dec"]
        if self.options.shared:
            self.cpp_info.defines.append("WOFF_DLL")

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "woff2")
        self.cpp_info.set_property("pkg_config_name", "woff2")

        self.cpp_info.components["woff2common"].set_property(
            "cmake_target_name", "woff2::woff2common")
        self.cpp_info.components["woff2common"].set_property(
            "pkg_config_name", "libwoff2common")
        self.cpp_info.components["woff2common"].libs = ["woff2common"]

        self.cpp_info.components["woff2enc"].set_property(
            "cmake_target_name", "woff2::woff2enc")
        self.cpp_info.components["woff2enc"].set_property(
            "pkg_config_name", "libwoff2enc")
        self.cpp_info.components["woff2enc"].libs = ["woff2enc"]
        self.cpp_info.components["woff2enc"].requires = ["woff2common"]

        self.cpp_info.components["woff2dec"].set_property(
            "cmake_target_name", "woff2::woff2dec")
        self.cpp_info.components["woff2dec"].set_property(
            "pkg_config_name", "libwoff2dec")
        self.cpp_info.components["woff2dec"].libs = ["woff2dec"]
        self.cpp_info.components["woff2dec"].requires = ["woff2common"]

        self.cpp_info.components["woff2common"].requires.append(
            "brotli::brotli")
