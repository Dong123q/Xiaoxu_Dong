program generate_sparse_matrices

implicit none
    
integer :: n, i, j, k, num_matrices, m
real, allocatable :: matrix(:,:) 
character(len=20) :: filename
integer, dimension(:), allocatable :: seed 
    
! The number of matrices to generate
num_matrices = 360

! open a file
filename = 'sparse_matrix.txt'
open(unit=10, file=filename, status='replace')

! Generate sparse matrix
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
		
		! Convert random numbers in matrix to sparse matrix
		do i = 1, n
			do m = 1, n
				! If the random number is less than 0.5, it is set to zero
				if (matrix(i, m) < 0.5) then
					matrix(i, m) = 0.0
				! Expand the random number to between 0 and 100
				else   
				   matrix(i, m) = int(matrix(i, m) * 100)
				end if
			end do
		end do
		
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

end program generate_sparse_matrices
