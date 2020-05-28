
/*!
@defgroup experiments-regfile-neighbour-hw-code Experiment Code
@{
@ingroup  experiments-regfile-neighbour-hw
*/

#include <stdlib.h>
#include <string.h>

#include "uas_bsp.h"

#include "experiment.h"

#define RLEN 4

//! Randomness array. Managed by SCASS.
uint8_t randomness[RLEN];

int di1_fixed,di1_rand ; //!< TTest random input values.

//! Variables which the SCASS framework can control.
scass_target_var  experiment_variables [] = {
{"di1" , 4, &di1_rand, &di1_fixed, SCASS_FLAGS_TTEST_IN},
};

//! Declaration for the experiment payload function in ldst-byte.S
extern void     * experiment_payload(
    int d1
);

//! Does nothing.
uint8_t experiment_init(
    scass_target_cfg * cfg //!< SCASS Framework configuration object.
) {
    return 0;
}

/*!
@details Runs the experiment, then finishes.
*/
uint8_t experiment_run(
    scass_target_cfg * cfg,  //!< SCASS Framework configuration object.
    char               fixed //!< used fixed variants of variables?
){

    int d1 = (fixed ? di1_fixed: di1_rand);

    uas_bsp_trigger_set();
    
    experiment_payload(
        d1
    );
    
    uas_bsp_trigger_clear();

    return 0;

}

void experiment_setup_scass(
    scass_target_cfg * cfg //!< The config object to setup.
){

    cfg -> scass_experiment_init = experiment_init;
    cfg -> scass_experiment_run  = experiment_run ;

    cfg -> experiment_name       = "regfile/shift-imm";

    cfg -> variables             = experiment_variables ;
    cfg -> variables[0].size = sizeof(int);
    cfg -> num_variables         = 1                    ;
    cfg -> randomness            = randomness;
    cfg -> randomness_len        = RLEN;
    cfg -> randomness_refresh_rate=0;

}

//! @}
