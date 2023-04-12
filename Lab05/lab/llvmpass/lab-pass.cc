/*
  Ref:
  * https://llvm.org/doxygen/
  * https://llvm.org/docs/GettingStarted.html
  * https://llvm.org/docs/WritingAnLLVMPass.html
  * https://llvm.org/docs/ProgrammersManual.html
 */
#include "lab-pass.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/GlobalVariable.h"
using namespace llvm;

char LabPass::ID = 0;
static FunctionCallee printfPrototype(Module &M);
static Constant* getI8StrVal(Module &M, char const *str, Twine const &name);

bool LabPass::doInitialization(Module &M) {
  return true;
}

bool LabPass::runOnModule(Module &M) {
  errs() << "runOnModule\n";
  LLVMContext &ctx = M.getContext();
  FunctionCallee printfCallee = printfPrototype(M);
  
  IRBuilder<> BuilderInit(ctx);
  GlobalVariable *depth = new GlobalVariable(M, Type::getInt32Ty(ctx), false,
    GlobalValue::ExternalLinkage, BuilderInit.getInt32(0), "depth");

  for (auto &F : M) {
    if (F.empty()) continue;
    errs() << F.getName() << "\n";

    IRBuilder<> BuilderStart(&F.getEntryBlock().front());
    Value *LoadDepth = BuilderStart.CreateLoad(Type::getInt32Ty(ctx), depth);

    const std::string message = "%*s%s: %p\n";
    Constant *space = getI8StrVal(M, "", "space");
    Constant *depthMsg = getI8StrVal(M, message.c_str(), "depthMsg");
    Constant *funcName = getI8StrVal(M, std::string(F.getName()).c_str(), "functionName");
    Constant *funcAddr = ConstantExpr::getBitCast(&F, Type::getInt8PtrTy(ctx));
    BuilderStart.CreateCall(printfCallee, { depthMsg, LoadDepth, space, funcName, funcAddr });

    Value *One = ConstantInt::get(Type::getInt32Ty(ctx), 1);
    Value *AddVal = BuilderStart.CreateAdd(One, LoadDepth);
    StoreInst *Store = BuilderStart.CreateStore(AddVal, depth);

    BasicBlock &Bend = F.back();
    Instruction &ret = *(++Bend.rend());
    IRBuilder<> BuilderEnd(&ret);
    Store = BuilderEnd.CreateStore(LoadDepth, depth);
  }
  
  return true;
}

static FunctionCallee printfPrototype(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
    Type::getInt32Ty(ctx),
    { Type::getInt8PtrTy(ctx), Type::getInt32Ty(ctx), Type::getInt8PtrTy(ctx), Type::getInt8PtrTy(ctx), Type::getInt8PtrTy(ctx)},
    true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}

static Constant* getI8StrVal(Module &M, char const *str, Twine const &name) {
  LLVMContext &ctx = M.getContext();

  Constant *strConstant = ConstantDataArray::getString(ctx, str);

  GlobalVariable *gvStr = new GlobalVariable(M, strConstant->getType(), true,
    GlobalValue::InternalLinkage, strConstant, name);

  Constant *zero = Constant::getNullValue(IntegerType::getInt32Ty(ctx));
  Constant *indices[] = { zero, zero };
  Constant *strVal = ConstantExpr::getGetElementPtr(Type::getInt8PtrTy(ctx),
    gvStr, indices, true);

  return strVal;
}

static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);