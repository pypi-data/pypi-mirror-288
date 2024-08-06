/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Enum Utility Definitions                                                   *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|* From: AMDGPU.td                                                            *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace amdgpu {
::llvm::StringRef stringifyMFMAPermB(MFMAPermB val) {
  switch (val) {
    case MFMAPermB::none: return "none";
    case MFMAPermB::bcast_first_32: return "bcast_first_32";
    case MFMAPermB::bcast_second_32: return "bcast_second_32";
    case MFMAPermB::rotate_16_right: return "rotate_16_right";
    case MFMAPermB::bcast_first_16: return "bcast_first_16";
    case MFMAPermB::bcast_second_16: return "bcast_second_16";
    case MFMAPermB::bcast_third_16: return "bcast_third_16";
    case MFMAPermB::bcast_fourth_16: return "bcast_fourth_16";
  }
  return "";
}

::std::optional<MFMAPermB> symbolizeMFMAPermB(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::std::optional<MFMAPermB>>(str)
      .Case("none", MFMAPermB::none)
      .Case("bcast_first_32", MFMAPermB::bcast_first_32)
      .Case("bcast_second_32", MFMAPermB::bcast_second_32)
      .Case("rotate_16_right", MFMAPermB::rotate_16_right)
      .Case("bcast_first_16", MFMAPermB::bcast_first_16)
      .Case("bcast_second_16", MFMAPermB::bcast_second_16)
      .Case("bcast_third_16", MFMAPermB::bcast_third_16)
      .Case("bcast_fourth_16", MFMAPermB::bcast_fourth_16)
      .Default(::std::nullopt);
}
::std::optional<MFMAPermB> symbolizeMFMAPermB(uint32_t value) {
  switch (value) {
  case 0: return MFMAPermB::none;
  case 1: return MFMAPermB::bcast_first_32;
  case 2: return MFMAPermB::bcast_second_32;
  case 3: return MFMAPermB::rotate_16_right;
  case 4: return MFMAPermB::bcast_first_16;
  case 5: return MFMAPermB::bcast_second_16;
  case 6: return MFMAPermB::bcast_third_16;
  case 7: return MFMAPermB::bcast_fourth_16;
  default: return ::std::nullopt;
  }
}

} // namespace amdgpu
} // namespace mlir

namespace mlir {
namespace amdgpu {
std::string stringifysched_barrier_opt_enum(sched_barrier_opt_enum symbol) {
  auto val = static_cast<uint32_t>(symbol);
  assert(2047u == (2047u | val) && "invalid bits set in bit enum");
  // Special case for all bits unset.
  if (val == 0) return "none";

  ::llvm::SmallVector<::llvm::StringRef, 2> strs;

  if (1u == (1u & val))
    strs.push_back("non_mem_non_sideffect");

  if (2u == (2u & val))
    strs.push_back("valu");

  if (4u == (4u & val))
    strs.push_back("salu");

  if (8u == (8u & val))
    strs.push_back("mfma_wmma");

  if (16u == (16u & val))
    strs.push_back("all_vmem");

  if (32u == (32u & val))
    strs.push_back("vmem_read");

  if (64u == (64u & val))
    strs.push_back("vmem_write");

  if (128u == (128u & val))
    strs.push_back("all_ds");

  if (256u == (256u & val))
    strs.push_back("ds_read");

  if (512u == (512u & val))
    strs.push_back("ds_write");

  if (1024u == (1024u & val))
    strs.push_back("transcendental");
  return ::llvm::join(strs, "|");
}

::std::optional<sched_barrier_opt_enum> symbolizesched_barrier_opt_enum(::llvm::StringRef str) {
  // Special case for all bits unset.
  if (str == "none") return sched_barrier_opt_enum::none;

  ::llvm::SmallVector<::llvm::StringRef, 2> symbols;
  str.split(symbols, "|");

  uint32_t val = 0;
  for (auto symbol : symbols) {
    auto bit = llvm::StringSwitch<::std::optional<uint32_t>>(symbol.trim())
      .Case("non_mem_non_sideffect", 1)
      .Case("valu", 2)
      .Case("salu", 4)
      .Case("mfma_wmma", 8)
      .Case("all_vmem", 16)
      .Case("vmem_read", 32)
      .Case("vmem_write", 64)
      .Case("all_ds", 128)
      .Case("ds_read", 256)
      .Case("ds_write", 512)
      .Case("transcendental", 1024)
      .Default(::std::nullopt);
    if (bit) { val |= *bit; } else { return ::std::nullopt; }
  }
  return static_cast<sched_barrier_opt_enum>(val);
}

::std::optional<sched_barrier_opt_enum> symbolizesched_barrier_opt_enum(uint32_t value) {
  // Special case for all bits unset.
  if (value == 0) return sched_barrier_opt_enum::none;

  if (value & ~static_cast<uint32_t>(2047u)) return std::nullopt;
  return static_cast<sched_barrier_opt_enum>(value);
}
} // namespace amdgpu
} // namespace mlir

