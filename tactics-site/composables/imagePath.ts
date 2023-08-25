export function get_image_path(names: string[]): string {
    const path = names.join('__')
    return `/image_${path}.jpg`
}