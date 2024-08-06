//-*-c++-*------------------------------------------------------------
//
// File name : bioExprLogLogit.h
// @date   Fri Apr 13 15:14:17 2018
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#ifndef bioExprLogLogit_h
#define bioExprLogLogit_h

#include <map>
#include "bioExpression.h"
#include "bioString.h"

class bioExprLogLogit: public bioExpression {
 public:
  bioExprLogLogit(bioExpression* c, std::map<bioUInt,bioExpression*> u, std::map<bioUInt,bioExpression*> a) ;
  ~bioExprLogLogit() ;
  virtual const bioDerivatives* getValueAndDerivatives(std::vector<bioUInt> literalIds,
						 bioBoolean gradient,
						bioBoolean hessian) ;
  virtual bioString print(bioBoolean hp = false) const ;
protected:
  bioExpression* choice ;
  std::map<bioUInt,bioExpression*> utilities ;
  std::map<bioUInt,bioExpression*> availabilities ;
  std::vector<bioDerivatives> Vs ;
  std::vector<bioReal> expi ;

  bioUInt chosen ;
  bioReal largestUtility ;
  bioReal av ;
  std::map<bioUInt,bioExpression*>::iterator theUtil ;
  bioReal shift ;
  bioReal denominator ;
  std::vector<bioReal> weightedSum ;
  bioReal dsquare ;
  bioReal dsecond ;
  bioReal the_term ;
  bioReal vih ;
  bioReal v, v1, v2 ;
};


#endif
