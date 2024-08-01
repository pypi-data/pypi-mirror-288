/*************************************************************************\
* Copyright (c) 2016 UChicago Argonne LLC, as Operator of Argonne
*     National Laboratory.
* Copyright (c) 2002 The Regents of the University of California, as
*     Operator of Los Alamos National Laboratory.
* SPDX-License-Identifier: EPICS
* EPICS BASE is distributed subject to a Software License Agreement found
* in file LICENSE that is included with this distribution.
\*************************************************************************/
/* dbConstLink.h
 *
 *  Created on: April 3rd, 2016
 *      Author: Andrew Johnson
 */

#ifndef INC_dbConstLink_H
#define INC_dbConstLink_H

#include "dbCoreAPI.h"

#ifdef __cplusplus
extern "C" {
#endif

struct link;

DBCORE_API void dbConstInitLink(struct link *plink);
DBCORE_API void dbConstAddLink(struct link *plink);

#ifdef __cplusplus
}
#endif

#endif /* INC_dbConstLink_H */

