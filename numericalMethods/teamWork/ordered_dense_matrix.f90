program generate_dense_matrices

implicit none

integer :: n, i, j, k, num_matrices, m
real, allocatable :: matrix(:,:) 
character(len=20) :: filename
integer, dimension(:), allocatable :: seed 

! The number of matrices to generate
num_matrices = 360

! open a file
filename = 'dense_matrix.txt'
open(unit=10, file=filename, status='replace')

! Generate dense matrix
do k = 3, 20
	n = k
	
	! Generate 20 matrices per size
	do j = 1, 20
		! Allocate matrix memory
		allocate(matrix(n,n))
		
		! Allocate and set random number seed
		allocate(seed(100))
		seed = [(n + j + m, m = 1, 100)]
		call random_seed(put=seed)
		
		! Generate random matrix
		call random_number(matrix)
		
		! Convert random numbers in matrix to integers
		matrix = nint(matrix * 100)
		
		! Write matrix dimensions to file
		write(10, '(I5)') n
		
		! Write matrix data to file
		do i = 1, n
			write(10, '(100I5)') (int(matrix(i, m)), m = 1, n) ! Write integer matrix to file
		end do
		
		! Write blank lines to separate different matrices
		write(10, *)
		
		! Release matrix memory
		deallocate(matrix)
		
		! Deallocate seed memory
		deallocate(seed)
	end do
end do

! Output extra 0 at end of file
write(10, *) '0'

! close file
close(10)

end program generate_dense_matrices
