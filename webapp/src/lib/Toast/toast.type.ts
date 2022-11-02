export type ToastType = {
	color: ToastColor;
	message: string;
};

export enum ToastColor {
	success = 'success',
	warning = 'warning',
	error = 'error',
}