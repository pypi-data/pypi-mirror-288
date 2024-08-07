// #define DEBUG 1
/*
 *  iaf_psc_exp_nestml.cpp
 *
 *  This file is part of NEST.
 *
 *  Copyright (C) 2004 The NEST Initiative
 *
 *  NEST is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  NEST is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with NEST.  If not, see <http://www.gnu.org/licenses/>.
 *
 *  Generated from NESTML at time: 2024-04-04 08:45:44.097960
**/

// C++ includes:
#include <limits>

// Includes from libnestutil:
#include "numerics.h"

// Includes from nestkernel:
#include "exceptions.h"
#include "kernel_manager.h"
#include "nest_impl.h"
#include "universal_data_logger_impl.h"

// Includes from sli:
#include "dict.h"
#include "dictutils.h"
#include "doubledatum.h"
#include "integerdatum.h"
#include "lockptrdatum.h"

#include "iaf_psc_exp_nestml.h"
void
register_iaf_psc_exp_nestml( const std::string& name )
{
  nest::register_node_model< iaf_psc_exp_nestml >( name );
}

// ---------------------------------------------------------------------------
//   Recordables map
// ---------------------------------------------------------------------------
nest::RecordablesMap<iaf_psc_exp_nestml> iaf_psc_exp_nestml::recordablesMap_;
namespace nest
{

  // Override the create() method with one call to RecordablesMap::insert_()
  // for each quantity to be recorded.
template <> void RecordablesMap<iaf_psc_exp_nestml>::create()
  {
    // add state variables to recordables map
   insert_(iaf_psc_exp_nestml_names::_V_m, &iaf_psc_exp_nestml::get_V_m);
   insert_(iaf_psc_exp_nestml_names::_I_noise, &iaf_psc_exp_nestml::get_I_noise);
   insert_(iaf_psc_exp_nestml_names::_psc_kernel__X__spikes, &iaf_psc_exp_nestml::get_psc_kernel__X__spikes);

    // Add vector variables  
  }
}

// ---------------------------------------------------------------------------
//   Default constructors defining default parameters and state
//   Note: the implementation is empty. The initialization is of variables
//   is a part of iaf_psc_exp_nestml's constructor.
// ---------------------------------------------------------------------------

iaf_psc_exp_nestml::Parameters_::Parameters_()
{
}

iaf_psc_exp_nestml::State_::State_()
{
}

// ---------------------------------------------------------------------------
//   Parameter and state extractions and manipulation functions
// ---------------------------------------------------------------------------

iaf_psc_exp_nestml::Buffers_::Buffers_(iaf_psc_exp_nestml &n):
  logger_(n)
  , spike_inputs_( std::vector< nest::RingBuffer >( NUM_SPIKE_RECEPTORS ) )
  , spike_inputs_grid_sum_( std::vector< double >( NUM_SPIKE_RECEPTORS ) )
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

iaf_psc_exp_nestml::Buffers_::Buffers_(const Buffers_ &, iaf_psc_exp_nestml &n):
  logger_(n)
  , spike_inputs_( std::vector< nest::RingBuffer >( NUM_SPIKE_RECEPTORS ) )
  , spike_inputs_grid_sum_( std::vector< double >( NUM_SPIKE_RECEPTORS ) )
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

// ---------------------------------------------------------------------------
//   Default constructor for node
// ---------------------------------------------------------------------------

iaf_psc_exp_nestml::iaf_psc_exp_nestml():StructuralPlasticityNode(), P_(), S_(), B_(*this)
{
  init_state_internal_();
  recordablesMap_.create();
  pre_run_hook();
}

// ---------------------------------------------------------------------------
//   Copy constructor for node
// ---------------------------------------------------------------------------

iaf_psc_exp_nestml::iaf_psc_exp_nestml(const iaf_psc_exp_nestml& __n):
  StructuralPlasticityNode(), P_(__n.P_), S_(__n.S_), B_(__n.B_, *this) {

  // copy parameter struct P_
  P_.E_L = __n.P_.E_L;
  P_.I_e = __n.P_.I_e;
  P_.tau_m = __n.P_.tau_m;
  P_.tau_syn = __n.P_.tau_syn;
  P_.C_m = __n.P_.C_m;
  P_.V_theta = __n.P_.V_theta;
  P_.mean_noise = __n.P_.mean_noise;
  P_.sigma_noise = __n.P_.sigma_noise;
  P_.tau_noise = __n.P_.tau_noise;

  // copy state struct S_
  S_.V_m = __n.S_.V_m;
  S_.I_noise = __n.S_.I_noise;
  S_.psc_kernel__X__spikes = __n.S_.psc_kernel__X__spikes;

  // copy internals V_
  V_.A_noise = __n.V_.A_noise;
  V_.__h = __n.V_.__h;
  V_.__P__V_m__V_m = __n.V_.__P__V_m__V_m;
  V_.__P__V_m__psc_kernel__X__spikes = __n.V_.__P__V_m__psc_kernel__X__spikes;
  V_.__P__psc_kernel__X__spikes__psc_kernel__X__spikes = __n.V_.__P__psc_kernel__X__spikes__psc_kernel__X__spikes;
}

// ---------------------------------------------------------------------------
//   Destructor for node
// ---------------------------------------------------------------------------

iaf_psc_exp_nestml::~iaf_psc_exp_nestml()
{
}

// ---------------------------------------------------------------------------
//   Node initialization functions
// ---------------------------------------------------------------------------
void iaf_psc_exp_nestml::calibrate_time( const nest::TimeConverter& tc )
{
  LOG( nest::M_WARNING,
    "iaf_psc_exp_nestml",
    "Simulation resolution has changed. Internal state and parameters of the model have been reset!" );

  init_state_internal_();
}
void iaf_psc_exp_nestml::init_state_internal_()
{
#ifdef DEBUG
  std::cout << "iaf_psc_exp_nestml::init_state_internal_()" << std::endl;
#endif

  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function
  // initial values for parameters
    

    P_.E_L = (-65); // as mV
    

    P_.I_e = 0; // as pA
    

    P_.tau_m = 25; // as ms
    

    P_.tau_syn = 5; // as ms
    

    P_.C_m = 250; // as pF
    

    P_.V_theta = (-30); // as mV
    

    P_.mean_noise = 0.057; // as pA
    

    P_.sigma_noise = 0.003; // as pA
    

    P_.tau_noise = 10; // as ms

  recompute_internal_variables();
  // initial values for state variables
    

    S_.V_m = P_.E_L; // as mV
    

    S_.I_noise = P_.mean_noise; // as pA
    

    S_.psc_kernel__X__spikes = 0; // as real
}

void iaf_psc_exp_nestml::init_buffers_()
{
#ifdef DEBUG
  std::cout << "iaf_psc_exp_nestml::init_buffers_()" << std::endl;
#endif
  // spike input buffers
  get_spike_inputs_().clear();
  get_spike_inputs_grid_sum_().clear();

  B_.logger_.reset();


}

void iaf_psc_exp_nestml::recompute_internal_variables(bool exclude_timestep) {
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function

  if (exclude_timestep) {    
      

      V_.A_noise = P_.sigma_noise * pow(((1 - std::exp((-2) * __resolution / P_.tau_noise))), 0.5); // as real
      

      V_.__P__V_m__V_m = 1.0 * std::exp((-V_.__h) / P_.tau_m); // as real
      

      V_.__P__V_m__psc_kernel__X__spikes = 1.0 * P_.tau_m * P_.tau_syn * ((-std::exp(V_.__h / P_.tau_m)) + std::exp(V_.__h / P_.tau_syn)) * std::exp((-V_.__h) * (P_.tau_m + P_.tau_syn) / (P_.tau_m * P_.tau_syn)) / (P_.C_m * (P_.tau_m - P_.tau_syn)); // as real
      

      V_.__P__psc_kernel__X__spikes__psc_kernel__X__spikes = 1.0 * std::exp((-V_.__h) / P_.tau_syn); // as real
  }
  else {    
      

      V_.A_noise = P_.sigma_noise * pow(((1 - std::exp((-2) * __resolution / P_.tau_noise))), 0.5); // as real
      

      V_.__h = __resolution; // as ms
      

      V_.__P__V_m__V_m = 1.0 * std::exp((-V_.__h) / P_.tau_m); // as real
      

      V_.__P__V_m__psc_kernel__X__spikes = 1.0 * P_.tau_m * P_.tau_syn * ((-std::exp(V_.__h / P_.tau_m)) + std::exp(V_.__h / P_.tau_syn)) * std::exp((-V_.__h) * (P_.tau_m + P_.tau_syn) / (P_.tau_m * P_.tau_syn)) / (P_.C_m * (P_.tau_m - P_.tau_syn)); // as real
      

      V_.__P__psc_kernel__X__spikes__psc_kernel__X__spikes = 1.0 * std::exp((-V_.__h) / P_.tau_syn); // as real
  }
}
void iaf_psc_exp_nestml::pre_run_hook() {
  B_.logger_.init();

  // parameters might have changed -- recompute internals
  recompute_internal_variables();

  // buffers B_
  B_.spike_inputs_.resize(NUM_SPIKE_RECEPTORS);
  B_.spike_inputs_grid_sum_.resize(NUM_SPIKE_RECEPTORS);
}

// ---------------------------------------------------------------------------
//   Update and spike handling functions
// ---------------------------------------------------------------------------


void iaf_psc_exp_nestml::update(nest::Time const & origin,const long from, const long to)
{
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function



  for ( long lag = from ; lag < to ; ++lag )
  {
    auto get_t = [origin, lag](){ return nest::Time( nest::Time::step( origin.get_steps() + lag + 1) ).get_ms(); };

    for (long i = 0; i < NUM_SPIKE_RECEPTORS; ++i)
    {
        get_spike_inputs_grid_sum_()[i] = get_spike_inputs_()[i].get_value(lag);
    }

    // NESTML generated code for the update block
  S_.I_noise = P_.mean_noise + (S_.I_noise - P_.mean_noise) * std::exp((-__resolution) / P_.tau_noise) + V_.A_noise * ((0) + (1) * normal_dev_( nest::get_vp_specific_rng( get_thread() ) ));
  double V_m__tmp = (-P_.E_L) * V_.__P__V_m__V_m + P_.E_L + S_.V_m * V_.__P__V_m__V_m + V_.__P__V_m__psc_kernel__X__spikes * S_.psc_kernel__X__spikes - P_.I_e * V_.__P__V_m__V_m * P_.tau_m / P_.C_m + P_.I_e * P_.tau_m / P_.C_m - S_.I_noise * V_.__P__V_m__V_m * P_.tau_m / P_.C_m + S_.I_noise * P_.tau_m / P_.C_m;
  double psc_kernel__X__spikes__tmp = V_.__P__psc_kernel__X__spikes__psc_kernel__X__spikes * S_.psc_kernel__X__spikes;
  /* replace analytically solvable variables with precisely integrated values  */
  S_.V_m = V_m__tmp;
  S_.psc_kernel__X__spikes = psc_kernel__X__spikes__tmp;
  S_.psc_kernel__X__spikes += ((0.001 * B_.spike_inputs_grid_sum_[SPIKES - MIN_SPIKE_RECEPTOR])) / (1 / 1000.0);
  if (S_.V_m > P_.V_theta)
  {  
    S_.V_m = P_.E_L;
    set_spiketime(nest::Time::step(origin.get_steps()+lag+1));
    nest::SpikeEvent se;
    nest::kernel().event_delivery_manager.send(*this, se, lag);
  }
    // voltage logging
    B_.logger_.record_data(origin.get_steps() + lag);
  }
}

// Do not move this function as inline to h-file. It depends on
// universal_data_logger_impl.h being included here.
void iaf_psc_exp_nestml::handle(nest::DataLoggingRequest& e)
{
  B_.logger_.handle(e);
}


void iaf_psc_exp_nestml::handle(nest::SpikeEvent &e)
{
  assert(e.get_delay_steps() > 0);
  assert( e.get_rport() < B_.spike_inputs_.size() );

  double weight = e.get_weight();
  size_t nestml_buffer_idx = 0;
  B_.spike_inputs_[ nestml_buffer_idx - MIN_SPIKE_RECEPTOR ].add_value(
    e.get_rel_delivery_steps( nest::kernel().simulation_manager.get_slice_origin() ),
    weight * e.get_multiplicity() );
}

