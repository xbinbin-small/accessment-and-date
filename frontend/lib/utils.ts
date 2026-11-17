import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

/** 合并 Tailwind 类名，后者覆盖冲突的工具类 */
export const cn = (...inputs: ClassValue[]) => twMerge(clsx(inputs))
