import useSWR from 'swr';
import {
  getDashboardStats,
  getJobs,
  getApplications,
  getStartups,
  getDealflow,
  getJobStats,
  getApplicationStats,
  getDealflowStats
} from '@/lib/api';

// Dashboard hook with auto-refresh every 30 seconds
export const useDashboard = () => {
  return useSWR('dashboard-stats', getDashboardStats, {
    refreshInterval: 30000, // Refresh every 30 seconds for real-time gamification
    revalidateOnFocus: true,
  });
};

// Jobs hooks
export const useJobs = (params?: any) => {
  const key = params ? ['jobs', JSON.stringify(params)] : 'jobs';
  return useSWR(key, () => getJobs(params));
};

export const useJobStats = () => {
  return useSWR('job-stats', getJobStats);
};

// Applications hooks
export const useApplications = (params?: any) => {
  const key = params ? ['applications', JSON.stringify(params)] : 'applications';
  return useSWR(key, () => getApplications(params));
};

export const useApplicationStats = () => {
  return useSWR('application-stats', getApplicationStats);
};

// Startups hooks
export const useStartups = (params?: any) => {
  const key = params ? ['startups', JSON.stringify(params)] : 'startups';
  return useSWR(key, () => getStartups(params));
};

// Dealflow hooks
export const useDealflow = (params?: any) => {
  const key = params ? ['dealflow', JSON.stringify(params)] : 'dealflow';
  return useSWR(key, () => getDealflow(params));
};

export const useDealflowStats = () => {
  return useSWR('dealflow-stats', getDealflowStats);
};
